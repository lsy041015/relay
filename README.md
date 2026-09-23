# Relay

Codex에서 설계·리뷰는 **사용자가 선택한 메인 모델과 추론 수준**으로 수행하고, 범위가 명확한 구현은 필요할 때 **GPT-6 Luna `xhigh` 구현자**에게 맡기는 스킬 플러그인입니다. [Jesse Vincent의 Superpowers](https://github.com/obra/superpowers) 6.4.1을 기반으로 한 개인 포크이며, 공식 OpenAI 또는 Superpowers 배포판은 아닙니다.

> **상태:** 개인 환경에서 검증 중인 실험판. 주간 Codex 사용량 절감은 아직 입증되지 않았습니다.

## 작동 방식

| 단계 | 담당 | 적용 |
|---|---|---|
| 요구사항 판단, 설계, 계획 | 메인 대화 | 현재 선택한 모델·추론 수준 유지 |
| 범위가 정해진 코드 수정과 관련 테스트 | 구현자 1명 | 호스트가 지원하면 `gpt-6-luna`, `xhigh`, `fork_turns="none"` |
| 코드 리뷰, 결과 통합, 최종 검증 | 메인 대화 | 현재 선택한 모델·추론 수준 유지 |

메인은 작은 수정이나 읽기 전용 작업을 직접 처리할 수 있습니다. 구현자를 만들면 필요한 목표·파일·제약·검증 기준만 전달하고, 관련 수정에 같은 구현자를 재사용합니다. 독립된 작업의 병렬 구현은 사용자가 명시적으로 요청한 경우에만 수행합니다. 별도 리뷰어·계획자·진단 에이전트와 중첩 위임은 사용하지 않습니다.

이 플러그인은 **15개 스킬과 보조 스크립트**로 구성됩니다. MCP 서버, 외부 계정 연결, 자동 실행 훅은 포함하지 않습니다. 모델 선택은 스킬이 에이전트에게 요청하는 운영 규칙입니다. 플러그인이 현재 대화의 모델을 바꾸거나 호스트의 모델 지원·권한을 강제하지는 않습니다.

| 용도 | 스킬 |
|---|---|
| 진입·설계·계획 | [using-superpowers](skills/using-superpowers/SKILL.md), [brainstorming](skills/brainstorming/SKILL.md), [writing-plans](skills/writing-plans/SKILL.md) |
| 구현·격리·테스트 | [subagent-driven-development](skills/subagent-driven-development/SKILL.md), [executing-plans](skills/executing-plans/SKILL.md), [using-git-worktrees](skills/using-git-worktrees/SKILL.md), [test-driven-development](skills/test-driven-development/SKILL.md) |
| 진단·검토·검증 | [systematic-debugging](skills/systematic-debugging/SKILL.md), [requesting-code-review](skills/requesting-code-review/SKILL.md), [receiving-code-review](skills/receiving-code-review/SKILL.md), [verification-before-completion](skills/verification-before-completion/SKILL.md), [diagnosing-superpowers](skills/diagnosing-superpowers/SKILL.md) |
| 종료·확장 | [finishing-a-development-branch](skills/finishing-a-development-branch/SKILL.md), [dispatching-parallel-agents](skills/dispatching-parallel-agents/SKILL.md), [writing-skills](skills/writing-skills/SKILL.md) |

## 설치

GitHub 저장소에 포함된 [Relay 마켓플레이스](.agents/plugins/marketplace.json)를 Codex에 등록합니다.

```bash
codex plugin marketplace add lsy041015/relay
codex plugin add superpowers-astra-luna@relay
```

Codex 플러그인 화면에서 `Relay` 소스를 선택해 설치해도 됩니다. 설치 후 **새 대화**를 시작해야 갱신된 스킬을 읽습니다. 기존 Superpowers 또는 개인 로컬판 `superpowers-astra-luna@personal`을 사용 중이라면 중복 활성화를 피하도록 한쪽만 활성화하세요. 저장소를 GitHub에 올리는 것과 OpenAI의 공개 플러그인 디렉터리에 게시하는 것은 별개입니다. 이 저장소는 GitHub 마켓플레이스 설치 경로를 제공합니다. 설치 구조는 [OpenAI 공식 플러그인 문서](https://developers.openai.com/plugins/build/plugins)를 따릅니다.

업데이트:

```bash
codex plugin marketplace upgrade relay
codex plugin add superpowers-astra-luna@relay
```

### 로컬 개발판

개발자는 원본을 `~/plugins/superpowers-astra-luna`처럼 원하는 위치에 복제하고 `~/.agents/plugins/marketplace.json`의 개인 마켓플레이스에 이 플러그인 항목을 추가할 수 있습니다. `source.path`는 `~/.agents/plugins/`가 아니라 **홈 디렉터리 기준** 상대 경로입니다. 예를 들어 원본이 `~/plugins/superpowers-astra-luna`에 있으면 `./plugins/superpowers-astra-luna`를 사용합니다. 기존 마켓플레이스 파일의 다른 항목은 보존하세요.

로컬 스킬을 고친 뒤에는 Codex의 `plugin-creator/scripts/update_plugin_cachebuster.py`로 버전의 캐시 식별자를 갱신하고 `codex plugin add superpowers-astra-luna@personal`로 재설치합니다. 설치 캐시를 직접 고치면 다음 업데이트에 사라집니다.

## 사용 예

```text
현재 메인 모델과 추론 수준으로 설계·리뷰해줘.
구현 범위가 정해지면 Relay 규칙에 따라 GPT-6 Luna xhigh 구현자에게 맡기고,
메인 대화에서 테스트 근거와 최종 변경을 확인해줘.
```

설계가 이미 정해진 작은 수정에는 별도 설계 승인 절차를 추가하지 않습니다. 다단계 작업에는 검증 가능한 계획을 남깁니다. 계획의 작업 제목은 `### Task 1: 입력 검증`처럼 작성하면 작업 추출기가 인식합니다. 코드 블록 안의 예시 제목은 작업 경계로 취급하지 않습니다.

검증은 실행 명령·대상 상태·종료 코드·결과를 확인합니다. 코드, 미커밋 변경, 신규 파일 또는 관련 환경이 달라졌으면 영향받은 검사를 다시 수행합니다. 실패한 검사를 통과로 요약하지 않습니다.

## 안전장치

- Relay가 만든 Git worktree의 Git 관리 디렉터리에 소유 표식을 기록합니다. [정리 절차](skills/finishing-a-development-branch/SKILL.md)는 표식과 실제 경로가 일치할 때만 해당 worktree를 제거합니다. 경로 이름만으로 사용자 worktree를 Relay 소유로 판단하지 않습니다.
- [SDD 작업공간 스크립트](skills/subagent-driven-development/scripts/sdd-workspace)는 작업공간 경로의 심볼릭 링크를 거부하고 기존 `.gitignore` 내용을 보존합니다.
- [작업 완료 스크립트](skills/executing-plans/scripts/task-done)는 테스트 명령이 성공하면 출력이 없어도 진행 기록을 남기며, 실패하면 완료로 기록하지 않습니다.

## 검증과 지원 범위

저장소 루트에서 실행:

```bash
python3 tests/test_task_brief.py
python3 tests/test_worktree_instructions.py
python3 tests/test_worktree_cleanup.py
python3 tests/test_sdd_safety.py
```

현재 회귀 검사 **16개**, 스킬 frontmatter 검사 **15개**, Bash 문법 검사 **8개**를 통과했습니다. 테스트는 작업 추출, 임시 Git 저장소에서의 worktree 생성·정리, SDD 경로 안전성, 출력 없는 성공 명령 기록을 다룹니다. 이 결과는 모든 스킬의 실제 모델 위임, 다중 운영체제, 모든 실패 복구 경로를 검증한 것은 아닙니다.

실행 경로에 따라 Git·Bash가 필요합니다. 회귀 검사는 Python 3 표준 라이브러리를 사용합니다. Git worktree 대체 절차는 GNU `realpath -m`을 사용하므로 해당 명령이 없는 환경에서는 호스트의 기본 worktree 기능을 우선 사용하세요. 시각적 설계 보조에는 Node.js가, 긴 세션 진단의 일부 경로에는 별도 `context-mode` 도구가 필요할 수 있습니다. `gpt-6-luna`와 `xhigh`가 호스트에서 지원되지 않으면 임의의 다른 모델로 바꾸지 않고 메인에서 처리하거나 제한을 알립니다.

## 주간 사용량 측정

Relay는 검토용 에이전트 생성과 전체 대화 복제를 줄이도록 설계됐습니다. **주간 한도 절감률은 아직 측정되지 않았고 보장되지 않습니다.** Codex 계정의 7일 창 사용률(`usedPercent`)이 비교 지표입니다. 적용 전의 완료된 7일 창 기준값이 없으며, 계정 전체 사용률에는 Relay 외 작업도 포함됩니다.

비교하려면 각 창의 종료 직전 사용률과 수행 작업량, 모델·추론 설정, 재시도와 검증 범위를 함께 기록해야 합니다. 토큰 수, 본문 길이, 실행 시간을 주간 한도 절감률로 환산하지 않습니다. 현재 자료로 절감률을 수치화하면 근거 없는 추정입니다.

## 이슈·출처

Relay 동작 문제는 [Relay Issues](https://github.com/lsy041015/relay/issues)에 보고하세요. 원본 Superpowers 문제를 상위 프로젝트에 보고할지는 별도로 판단해야 합니다.

원본: [Jesse Vincent의 Superpowers](https://github.com/obra/superpowers) 6.4.1. 원본 저작권과 [MIT 라이선스](LICENSE)를 보존했습니다. 원본 설명은 [UPSTREAM_README.md](UPSTREAM_README.md)에 있습니다. 이 포크의 운영 규칙은 현재 README와 `skills/`를 따릅니다.
