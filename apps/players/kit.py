from apps.objects.models.object_mod import ObjectObjectMod

from .models.object import PlayerObject, PositionType, PositionValue


# Head-to-feet paperdoll order, held items in their worn position — the same
# presentation order the HUD uses for recipe categories (docs/design ADR).
KIT_SLOTS = (
    (PositionValue.EQUIPPED_ON_FOREHEAD, "Forehead", "gem"),
    (PositionValue.EQUIPPED_ON_HEAD, "Head", "record-circle"),
    (PositionValue.EQUIPPED_ON_FACE, "Face", "sunglasses"),
    (PositionValue.EQUIPPED_IN_MOUTH, "Mouth", "emoji-smile"),
    (PositionValue.EQUIPPED_ON_NECK, "Neck", "link-45deg"),
    (PositionValue.EQUIPPED_ON_NECK_ALT, "Neck ②", "link-45deg"),
    (PositionValue.EQUIPPED_ABOUT, "About", "layers"),
    (PositionValue.EQUIPPED_ON_BACK, "Back", "backpack2"),
    (PositionValue.EQUIPPED_ON_BACK_ALT, "Back ②", "backpack2"),
    (PositionValue.EQUIPPED_ON_BODY, "Body", "person-standing"),
    (PositionValue.EQUIPPED_ON_UPPER_BODY, "Upper Body", "person-arms-up"),
    (PositionValue.EQUIPPED_ON_CHEST, "Chest", "shield-shaded"),
    (PositionValue.EQUIPPED_ON_ARMS, "Arms", "grip-vertical"),
    (PositionValue.EQUIPPED_ON_HANDS, "Hands", "hand-index-thumb"),
    (PositionValue.EQUIPPED_ON_LEFT_WRIST, "Left Wrist", "watch"),
    (PositionValue.EQUIPPED_ON_RIGHT_WRIST, "Right Wrist", "watch"),
    (PositionValue.EQUIPPED_ON_LEFT_FINGER, "Left Finger", "suit-diamond"),
    (PositionValue.EQUIPPED_ON_RIGHT_FINGER, "Right Finger", "suit-diamond"),
    (PositionValue.WIELDING, "Wielded", "lightning-charge"),
    (PositionValue.WIELDING_IN_TWO, "Two-Handed", "lightning"),
    (PositionValue.HELD_IN_LEFT_HAND, "Left Hand", "hand-index"),
    (PositionValue.HELD_IN_RIGHT_HAND, "Right Hand", "hand-index"),
    (PositionValue.EQUIPPED_ON_WAIST, "Waist", "dash-circle"),
    (PositionValue.EQUIPPED_ON_LEGS, "Legs", "person-walking"),
    (PositionValue.EQUIPPED_ON_FEET, "Feet", "person-walking"),
)


def build_kit(player) -> list:
    """Slot dicts for every wear position, worn item and its mods attached."""
    worn = {}
    for player_object in PlayerObject.objects.filter(
        player=player,
        position_type=PositionType.EQUIPMENT,
    ).select_related("object", "object__flag", "enchant"):
        worn.setdefault(player_object.position_val, player_object)

    # ObjectObjectMod's "object" relation is a OneToOne onto a composite-key
    #   table (multiple mod slots per vnum), so the reverse accessor lies —
    #   query the through table directly and group by vnum.
    mods = {}
    vnums = {po.object_id for po in worn.values()}
    if vnums:
        for object_mod in ObjectObjectMod.objects.filter(
            object_id__in=vnums,
        ).select_related("object_mod").order_by("mod_slot"):
            mods.setdefault(object_mod.object_id, []).append(object_mod)

    kit = []
    for position, label, icon in KIT_SLOTS:
        item = worn.get(int(position))
        kit.append({
            "position": int(position),
            "label": label,
            "icon": icon,
            "item": item,
            "mods": mods.get(item.object_id, ()) if item else (),
        })
    return kit
