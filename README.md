# VR360 Room

Unreal Engine 5.6 project for viewing equirectangular 360-degree panoramas on Meta Quest through OpenXR.

## Project

- Project file: `VR360Room.uproject`
- Startup map: `/Game/VR360/Maps/VR360Map`
- Active material: `/Game/VR360/Materials/M_BazaarPanorama_Unlit`
- Active panorama: `/Game/VR360/Textures/T_BazaarPanorama_3K`
- Android package: `com.codex.vr360room`

## Requirements

- Unreal Engine 5.6
- Android SDK configured for Meta Quest development
- Git LFS

Clone the repository with Git LFS enabled:

```powershell
git lfs install
git clone <repository-url>
```

Open `VR360Room.uproject` in Unreal Engine. Generated directories and packaged Android builds are intentionally excluded from version control and are recreated locally.

Additional project and device notes are in `HANDOFF_VR360_RU.md`.
