using UnrealBuildTool;

public class VR360RoomEditorTarget : TargetRules
{
    public VR360RoomEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_6;
        ExtraModuleNames.Add("VR360Room");
    }
}
