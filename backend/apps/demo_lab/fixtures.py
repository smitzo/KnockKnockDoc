import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from django.conf import settings


FIXTURE_DIRECTORY = Path(settings.BASE_DIR) / "fixtures" / "product_demo"
EXPECTED_SCHEMA_VERSION = 1
EXPECTED_FIXTURE_ID = "product-demo-v1"
REQUIRED_COLLECTIONS = {
    "organizations",
    "access_accounts",
    "doctors",
    "patients",
    "access_professional_profiles",
    "professional_ratings",
    "referral_workspace",
}
SECRET_KEYS = {
    "api_key",
    "credential",
    "password",
    "private_key",
    "secret",
    "token",
}


class DemoFixtureError(ValueError):
    pass


@dataclass(frozen=True)
class ProductDemoFixture:
    manifest: dict[str, Any]
    organizations: list[dict[str, Any]]
    access_accounts: list[dict[str, Any]]
    doctors: list[dict[str, Any]]
    patients: list[dict[str, Any]]
    access_professional_profiles: list[dict[str, Any]]
    professional_ratings: list[dict[str, Any]]
    referral_workspace: dict[str, Any]

    @property
    def fixture_id(self) -> str:
        return str(self.manifest["fixture_id"])

    @property
    def schema_version(self) -> int:
        return int(self.manifest["schema_version"])

    @property
    def expected_counts(self) -> dict[str, int]:
        return dict(self.manifest["expected_counts"])

    @property
    def participant_emails(self) -> list[str]:
        return [
            str(item["login_email"])
            for item in [*self.access_accounts, *self.doctors, *self.patients]
        ]


def load_product_demo_fixture() -> ProductDemoFixture:
    manifest = _read_json(FIXTURE_DIRECTORY / "manifest.json")
    if not isinstance(manifest, dict):
        raise DemoFixtureError("The demo fixture manifest must be a JSON object.")
    if manifest.get("schema_version") != EXPECTED_SCHEMA_VERSION:
        raise DemoFixtureError("The demo fixture schema version is unsupported.")
    if manifest.get("fixture_id") != EXPECTED_FIXTURE_ID:
        raise DemoFixtureError("The demo fixture identifier is unexpected.")
    if manifest.get("synthetic_only") is not True:
        raise DemoFixtureError("The demo fixture must declare synthetic_only=true.")

    file_map = manifest.get("files")
    if not isinstance(file_map, dict) or set(file_map) != REQUIRED_COLLECTIONS:
        raise DemoFixtureError("The demo fixture manifest has an incomplete file map.")

    loaded: dict[str, Any] = {}
    for collection_name, file_name in file_map.items():
        if not isinstance(file_name, str) or Path(file_name).name != file_name:
            raise DemoFixtureError("Demo fixture paths must be local file names.")
        loaded[collection_name] = _read_json(FIXTURE_DIRECTORY / file_name)

    list_collections = REQUIRED_COLLECTIONS - {"referral_workspace"}
    for collection_name in list_collections:
        if not isinstance(loaded[collection_name], list):
            raise DemoFixtureError(f"Fixture collection {collection_name} must be a JSON array.")
        _validate_collection(collection_name, loaded[collection_name])

    referral_workspace = loaded["referral_workspace"]
    if not isinstance(referral_workspace, dict):
        raise DemoFixtureError("The referral workspace fixture must be a JSON object.")
    if referral_workspace.get("synthetic_only") is not True:
        raise DemoFixtureError("The referral workspace must be explicitly synthetic.")

    _reject_secret_keys(manifest)
    for value in loaded.values():
        _reject_secret_keys(value)
    _validate_expected_counts(manifest, loaded)
    _validate_references(loaded)

    return ProductDemoFixture(manifest=manifest, **loaded)


def _read_json(path: Path) -> Any:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DemoFixtureError(f"Demo fixture file is unavailable: {path.name}.") from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise DemoFixtureError(f"Demo fixture file is invalid JSON: {path.name}.") from exc


def _validate_collection(collection_name: str, collection: list[dict[str, Any]]) -> None:
    fixture_keys: set[str] = set()
    for item in collection:
        if not isinstance(item, dict):
            raise DemoFixtureError(f"Fixture collection {collection_name} contains a non-object.")
        fixture_key = item.get("fixture_key")
        if not isinstance(fixture_key, str) or not fixture_key:
            raise DemoFixtureError(f"Fixture collection {collection_name} has a missing key.")
        if fixture_key in fixture_keys:
            raise DemoFixtureError(f"Fixture collection {collection_name} has a duplicate key.")
        fixture_keys.add(fixture_key)
        if item.get("is_synthetic") is not True:
            raise DemoFixtureError(
                f"Fixture collection {collection_name} contains a non-synthetic record."
            )


def _validate_expected_counts(manifest: dict[str, Any], loaded: dict[str, Any]) -> None:
    expected = manifest.get("expected_counts")
    if not isinstance(expected, dict):
        raise DemoFixtureError("The demo fixture manifest requires expected counts.")
    actual = {
        "organizations": len(loaded["organizations"]),
        "access_accounts": len(loaded["access_accounts"]),
        "doctors": len(loaded["doctors"]),
        "patients": len(loaded["patients"]),
        "access_professional_profiles": len(loaded["access_professional_profiles"]),
        "professional_ratings": len(loaded["professional_ratings"]),
        "referral_workspaces": 1,
    }
    if expected != actual:
        raise DemoFixtureError("The demo fixture record counts do not match its manifest.")


def _validate_references(loaded: dict[str, Any]) -> None:
    organizations = {item["fixture_key"] for item in loaded["organizations"]}
    accounts = {
        item["fixture_key"]: item
        for item in [*loaded["access_accounts"], *loaded["doctors"], *loaded["patients"]]
    }
    professional_keys = {
        *[item["fixture_key"] for item in loaded["doctors"]],
        *[item["fixture_key"] for item in loaded["access_professional_profiles"]],
    }
    for account in accounts.values():
        if account["organization_fixture_key"] not in organizations:
            raise DemoFixtureError("A demo account references an unknown organization.")
    for profile in loaded["access_professional_profiles"]:
        if profile["fixture_key"] not in accounts:
            raise DemoFixtureError("A professional profile references an unknown account.")
    for rating in loaded["professional_ratings"]:
        if {
            rating["subject_profile_fixture_key"],
            rating["reviewer_profile_fixture_key"],
        } - professional_keys:
            raise DemoFixtureError("A professional rating references an unknown profile.")
    for grant in loaded["referral_workspace"].get("access_grants", []):
        if grant.get("account_fixture_key") not in accounts:
            raise DemoFixtureError("A referral access grant references an unknown account.")


def _reject_secret_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).strip().lower().replace("-", "_")
            if normalized_key in SECRET_KEYS:
                raise DemoFixtureError("Credentials and secret material are forbidden in fixtures.")
            _reject_secret_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            _reject_secret_keys(nested)
