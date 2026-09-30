using UnrealBuildTool;

public class VR360RoomTarget : TargetRules
{
    public VR360RoomTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_6;
        ExtraModuleNames.Add("VR360Room");
    }
}
