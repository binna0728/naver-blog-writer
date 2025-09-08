클로드 코드 네이티브 윈도우 버전 설치 방법입니다.
(MCP 자동 설치를 위한 지침은 이 댓글의 답글 참조하세요)

1단계: Git for Windows 설치

# Git for Windows 다운로드 및 설치
https://git-scm.com/download/win 에서 다운로드


2단계: Node.js 설치

# Node.js 18+ 버전 설치
https://nodejs.org 에서 LTS 버전 다운로드


3단계: Claude Code 설치
#명령프롬프트 또는 파워셀에서 아래 명령어 넣고 엔터키
npm install -g @anthropic-ai/claude-code@latest


4단계: Git PATH 추가하기
(영상참조)

참고: Node.js는 디폴트 상태로 설치시 자동으로 PATH 추가됩니다

### WSL 사용하지 않는 경우, WSL 삭제하여 컴퓨터 리소스 확보하기 ###
(파워셀에서 다음 명령어 실행하기)
wsl --uninstall

(파워셸에서 다음 명령어 붙여 넣고 엔터를 누르기)

Get-ChildItem HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Lxss |
  ForEach-Object {
      $p = Get-ItemProperty $_.PsPath
      [PSCustomObject]@{
          Name     = $p.DistributionName
          BasePath = $p.BasePath
      }
  }

그럼 폴더 경로가 나오는데, 이 경로로 파일 탐색기에 들어가면 나오는 ext4 파일 삭제하기