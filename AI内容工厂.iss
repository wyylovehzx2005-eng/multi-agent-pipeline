; ============================================================
; AI内容工厂 - Inno Setup 安装包脚本（正式版）
; ============================================================

[Setup]
AppName=AI内容工厂
AppVersion=1.0
AppPublisher=ai第一观察者
DefaultDirName={autopf}\AI内容工厂
DefaultGroupName=AI内容工厂
OutputDir=D:\python-code\Multi-Agent Pipeline one\安装包
OutputBaseFilename=AI内容工厂_安装程序
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "发布包\AI内容工厂.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "发布包\使用说明.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AI内容工厂"; Filename: "{app}\AI内容工厂.exe"
Name: "{autodesktop}\AI内容工厂"; Filename: "{app}\AI内容工厂.exe"

[Run]
Filename: "{app}\AI内容工厂.exe"; Description: "立即运行 AI内容工厂"; Flags: nowait postinstall skipifsilent