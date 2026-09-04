from .models import ProductMode, ProductModeState


PRODUCT_MODE_KEY = "primary"


def current_product_mode() -> str:
    return (
        ProductModeState.objects.filter(key=PRODUCT_MODE_KEY)
        .values_list("mode", flat=True)
        .first()
        or ProductMode.STANDARD
    )


def is_demo_mode_enabled() -> bool:
    return current_product_mode() == ProductMode.DEMO


def lock_demo_mode_enabled() -> bool:
    state = (
        ProductModeState.objects.select_for_update()
        .filter(key=PRODUCT_MODE_KEY)
        .only("mode")
        .first()
    )
    return bool(state and state.mode == ProductMode.DEMO)
