import unreal
import os

PROJECT_ROOT = unreal.Paths.project_dir()
ASSET_TOOLS = unreal.AssetToolsHelpers.get_asset_tools()
EDITOR_ASSETS = unreal.EditorAssetLibrary

def log(message):
    unreal.log("[VR360] " + message)

def ensure_folder(path):
    if not EDITOR_ASSETS.does_directory_exist(path):
        EDITOR_ASSETS.make_directory(path)

def import_texture():
    source = os.path.join(PROJECT_ROOT, "Content", "VR360", "Textures", "T_Room360_8K.jpg")
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", source)
    task.set_editor_property("destination_path", "/Game/VR360/Textures")
    task.set_editor_property("destination_name", "T_Room360_8K")
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("automated", True)
    task.set_editor_property("save", True)
    ASSET_TOOLS.import_asset_tasks([task])
    texture = EDITOR_ASSETS.load_asset("/Game/VR360/Textures/T_Room360_8K")
    if not texture:
        raise RuntimeError("Unable to import T_Room360_8K.jpg")
    try:
        texture.set_editor_property("never_stream", True)
    except Exception:
        pass
    EDITOR_ASSETS.save_asset(texture.get_path_name())
    return texture

def create_material(texture):
    path = "/Game/VR360/Materials"
    ensure_folder(path)
    old = EDITOR_ASSETS.load_asset(path + "/M_VR360_Unlit")
    if old:
        EDITOR_ASSETS.delete_asset(path + "/M_VR360_Unlit")
    factory = unreal.MaterialFactoryNew()
    material = ASSET_TOOLS.create_asset("M_VR360_Unlit", path, unreal.Material, factory)
    material.set_editor_property("material_domain", unreal.MaterialDomain.MD_SURFACE)
    material.set_editor_property("blend_mode", unreal.BlendMode.BLEND_OPAQUE)
    material.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    material.set_editor_property("two_sided", True)
    sample = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionTextureSampleParameter2D, -300, 0)
    sample.set_editor_property("texture", texture)
    sample.set_editor_property("parameter_name", "Room360")
    unreal.MaterialEditingLibrary.connect_material_property(
        sample, "RGB", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    unreal.MaterialEditingLibrary.recompile_material(material)
    EDITOR_ASSETS.save_asset(material.get_path_name())
    return material

def create_game_mode():
    path = "/Game/VR360/Blueprints"
    ensure_folder(path)
    asset_path = path + "/BP_VR360GameMode"
    old = EDITOR_ASSETS.load_asset(asset_path)
    if old:
        EDITOR_ASSETS.delete_asset(asset_path)
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", unreal.GameModeBase)
    blueprint = ASSET_TOOLS.create_asset("BP_VR360GameMode", path, unreal.Blueprint, factory)
    generated_class = blueprint.generated_class()
    cdo = unreal.get_default_object(generated_class)
    cdo.set_editor_property("default_pawn_class", unreal.DefaultPawn)
    EDITOR_ASSETS.save_asset(blueprint.get_path_name())
    return generated_class

def create_level(material, game_mode_class):
    map_path = "/Game/VR360/Maps/VR360Map"
    ensure_folder("/Game/VR360/Maps")
    if EDITOR_ASSETS.does_asset_exist(map_path):
        unreal.EditorLevelLibrary.load_level(map_path)
    else:
        unreal.EditorLevelLibrary.new_level(map_path)
    for actor in unreal.EditorLevelLibrary.get_all_level_actors():
        if actor.get_actor_label() in ["VR360 Room Sphere", "VR Center"]:
            actor.destroy_actor()
    sphere = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
    sphere.set_actor_label("VR360 Room Sphere")
    sphere.set_actor_scale3d(unreal.Vector(1000, 1000, 1000))
    mesh = unreal.load_asset("/Engine/BasicShapes/Sphere")
    component = sphere.static_mesh_component
    component.set_editor_property("static_mesh", mesh)
    component.set_material(0, material)
    component.set_editor_property("cast_shadow", False)
    component.set_editor_property("mobility", unreal.ComponentMobility.STATIC)
    start = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
    start.set_actor_label("VR Center")
    settings = unreal.get_default_object(unreal.GameMapsSettings)
    map_soft_path = unreal.SoftObjectPath(map_path)
    settings.set_editor_property("editor_startup_map", map_soft_path)
    settings.set_editor_property("game_default_map", map_soft_path)
    settings.set_editor_property(
        "global_default_game_mode",
        unreal.SoftClassPath("/Game/VR360/Blueprints/BP_VR360GameMode.BP_VR360GameMode_C"))
    unreal.EditorLevelLibrary.save_current_level()
    return map_path

def main():
    log("Importing panorama texture")
    texture = import_texture()
    log("Creating two-sided unlit panorama material")
    material = create_material(texture)
    log("Creating default game mode")
    game_mode = create_game_mode()
    log("Building VR360 map")
    map_path = create_level(material, game_mode)
    log("READY " + map_path)
    unreal.SystemLibrary.quit_editor()

main()
