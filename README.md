# Relay

**Codex**와 **Claude Code** 양쪽에서 쓰는 스킬 플러그인입니다. 설계·리뷰·통합은 **사용자가 선택한 메인 모델과 추론 수준**으로 수행하고, 범위가 명확한 구현만 필요할 때 **호스트별 구현자 서브에이전트**에게 맡깁니다.

| 호스트 | 구현자 프리셋 |
|---|---|
| Codex | `gpt-6-luna` · `reasoning_effort = "xhigh"` · `fork_turns = "none"` |
| Claude Code | `relay:implementer` 에이전트 · `model: claude-sonnet-5` · `effort: high` |

[Jesse Vincent의 Superpowers](https://github.com/obra/superpowers) 6.4.1을 기반으로 한 개인 포크이며, 공식 OpenAI·Anthropic 또는 Superpowers 배포판은 아닙니다.

> **상태:** 개인 환경에서 검증 중인 실험판. 사용량 절감 효과는 아직 입증되지 않았습니다.

## 작동 방식

| 단계 | 담당 | 적용 |
|---|---|---|
| 요구사항 판단, 설계, 계획 | 메인 대화 | 현재 선택한 모델·추론 수준 유지 |
| 범위가 정해진 코드 수정과 관련 테스트 | 구현자 1명 | 위 표의 호스트별 구현자 프리셋 |
| 코드 리뷰, 결과 통합, 최종 검증 | 메인 대화 | 현재 선택한 모델·추론 수준 유지 |

메인은 작은 수정이나 읽기 전용 작업을 직접 처리할 수 있습니다. 구현자를 만들면 필요한 목표·파일·제약·검증 기준만 전달하고(이전 대화 기록은 넘기지 않음), 관련 수정에는 같은 구현자를 재사용합니다. 독립된 작업의 병렬 구현은 사용자가 명시적으로 요청한 경우에만 수행합니다. 별도 리뷰어·계획자·진단 에이전트와 중첩 위임은 사용하지 않습니다.

이 플러그인은 **15개 스킬, 보조 스크립트, Claude Code용 구현자 에이전트 1개**로 구성됩니다. MCP 서버, 외부 계정 연결, 자동 실행 훅은 포함하지 않습니다. 모델 선택은 스킬이 에이전트에게 요청하는 운영 규칙이며, 플러그인이 메인 대화의 모델을 바꾸지는 않습니다.

| 용도 | 스킬 |
|---|---|
| 진입·설계·계획 | [using-superpowers](skills/using-superpowers/SKILL.md), [brainstorming](skills/brainstorming/SKILL.md), [writing-plans](skills/writing-plans/SKILL.md) |
| 구현·격리·테스트 | [subagent-driven-development](skills/subagent-driven-development/SKILL.md), [executing-plans](skills/executing-plans/SKILL.md), [using-git-worktrees](skills/using-git-worktrees/SKILL.md), [test-driven-development](skills/test-driven-development/SKILL.md) |
| 진단·검토·검증 | [systematic-debugging](skills/systematic-debugging/SKILL.md), [requesting-code-review](skills/requesting-code-review/SKILL.md), [receiving-code-review](skills/receiving-code-review/SKILL.md), [verification-before-completion](skills/verification-before-completion/SKILL.md), [diagnosing-superpowers](skills/diagnosing-superpowers/SKILL.md) |
| 종료·확장 | [finishing-a-development-branch](skills/finishing-a-development-branch/SKILL.md), [dispatching-parallel-agents](skills/dispatching-parallel-agents/SKILL.md), [writing-skills](skills/writing-skills/SKILL.md) |

## 저장소 구조

```text
relay/
├── .claude-plugin/          # Claude Code 플러그인 매니페스트 + 마켓플레이스
│   ├── plugin.json
│   └── marketplace.json
├── .codex-plugin/           # Codex 플러그인 매니페스트
│   └── plugin.json
├── .agents/plugins/         # Codex 마켓플레이스
│   └── marketplace.json
├── agents/
│   └── implementer.md       # Claude Code 구현자 (claude-sonnet-5 / high)
├── skills/                  # 양쪽 공용 스킬 (SKILL.md 포맷 동일)
│   ├── */agents/openai.yaml # Codex UI 표시 정보 (Claude Code는 무시)
│   └── using-superpowers/references/
│       ├── codex-tools.md       # Codex 호출 문법 (spawn_agent, followup_task)
│       └── claude-code-tools.md # Claude Code 호출 문법 (Agent, SendMessage)
└── tests/
```

두 호스트 모두 플러그인 이름은 `relay`이며, 스킬 간 참조는 `relay:<skill>` 네임스페이스를 씁니다.

## 설치 — Claude Code

```bash
claude plugin marketplace add lsy041015/relay
claude plugin install relay@relay
```

또는 Claude Code 대화창에서 `/plugin marketplace add lsy041015/relay` → `/plugin install relay@relay`. 설치 후 **새 세션**을 시작하면 `relay:*` 스킬과 `relay:implementer` 에이전트가 활성화됩니다.

확인:

```bash
claude plugin list
```

구현자 호출 형태 (스킬이 자동으로 수행):

```text
Agent(subagent_type="relay:implementer", description="Implement task 2",
      prompt="<목표, 허용 파일, 인수 조건, 테스트, 리포트 경로>")
```

후속 수정은 같은 구현자에게 `SendMessage`로 보냅니다. `model`을 덮어쓰지 않습니다 — 모델·추론 수준은 [agents/implementer.md](agents/implementer.md)의 frontmatter가 고정합니다. 다른 모델을 쓰고 싶으면 이 파일의 `model`/`effort`만 바꾸면 됩니다.

업데이트:

```bash
claude plugin marketplace update relay
claude plugin install relay@relay
```

## 설치 — Codex

```bash
codex plugin marketplace add lsy041015/relay
codex plugin add relay@relay
```

Codex 플러그인 화면에서 `Relay` 소스를 선택해 설치해도 됩니다. 설치 후 **새 대화**를 시작해야 갱신된 스킬을 읽습니다.

> **이전 버전에서 옮기는 경우:** 플러그인 이름이 `superpowers-astra-luna`에서 `relay`로 바뀌었습니다. 기존 `superpowers-astra-luna@relay`(또는 `@personal`)는 비활성화·제거한 뒤 `relay@relay`를 설치하세요. 원본 Superpowers와도 중복 활성화하지 마세요.

업데이트:

```bash
codex plugin marketplace upgrade relay
codex plugin add relay@relay
```

### Codex 로컬 개발판

원본을 `~/plugins/relay`처럼 원하는 위치에 복제하고 `~/.agents/plugins/marketplace.json`의 개인 마켓플레이스에 항목을 추가합니다. `source.path`는 **홈 디렉터리 기준** 상대 경로입니다(예: `./plugins/relay`). 스킬을 고친 뒤에는 Codex의 `plugin-creator/scripts/update_plugin_cachebuster.py`로 캐시 식별자를 갱신하고 `codex plugin add relay@personal`로 재설치합니다. 설치 캐시를 직접 고치면 다음 업데이트에 사라집니다.

### Claude Code 로컬 개발판

```bash
git clone https://github.com/lsy041015/relay.git
claude plugin marketplace add ./relay
claude plugin install relay@relay
claude plugin validate ./relay
```

## 사용 예

Claude Code:

```text
현재 메인 모델로 설계·리뷰해줘. 구현 범위가 정해지면 Relay 규칙에 따라
relay:implementer(Sonnet 5 high)에게 맡기고, 메인에서 테스트 근거와 최종 변경을 확인해줘.
```

Codex:

```text
현재 메인 모델과 추론 수준으로 설계·리뷰해줘.
구현 범위가 정해지면 Relay 규칙에 따라 GPT-6 Luna xhigh 구현자에게 맡기고,
메인 대화에서 테스트 근거와 최종 변경을 확인해줘.
```

설계가 이미 정해진 작은 수정에는 별도 설계 승인 절차를 추가하지 않습니다. 다단계 작업에는 검증 가능한 계획을 남깁니다. 계획의 작업 제목은 `### Task 1: 입력 검증`처럼 작성하면 작업 추출기가 인식합니다. 코드 블록 안의 예시 제목은 작업 경계로 취급하지 않습니다.

검증은 실행 명령·대상 상태·종료 코드·결과를 확인합니다. 코드, 미커밋 변경, 신규 파일 또는 관련 환경이 달라졌으면 영향받은 검사를 다시 수행합니다. 실패한 검사를 통과로 요약하지 않습니다.

## 안전장치

- Relay가 만든 Git worktree의 Git 관리 디렉터리에 소유 표식을 기록합니다. [정리 절차](skills/finishing-a-development-branch/SKILL.md)는 표식과 실제 경로가 일치할 때만 해당 worktree를 제거합니다.
- [SDD 작업공간 스크립트](skills/subagent-driven-development/scripts/sdd-workspace)는 작업공간 경로의 심볼릭 링크를 거부하고 기존 `.gitignore` 내용을 보존합니다.
- [작업 완료 스크립트](skills/executing-plans/scripts/task-done)는 테스트 명령이 성공하면 출력이 없어도 진행 기록을 남기며, 실패하면 완료로 기록하지 않습니다.
- Claude Code 구현자는 `disallowedTools: Agent`로 하위 에이전트를 만들 수 없습니다.
- 호스트가 구현자 프리셋을 지원하지 않으면(모델 미지원, 에이전트 미설치) 임의의 다른 모델로 바꾸지 않고 메인에서 처리하거나 제한을 알립니다.

## 검증과 지원 범위

저장소 루트에서 실행:

```bash
python3 tests/test_task_brief.py
python3 tests/test_worktree_instructions.py
python3 tests/test_worktree_cleanup.py
python3 tests/test_sdd_safety.py
```

Linux·macOS에서 회귀 검사 **16개**, 스킬 frontmatter 검사 **15개**, Bash 문법 검사 **8개**를 통과했습니다. **Windows(Git Bash)에서는 현재 일부 실패합니다** — cp949 기본 인코딩(`PYTHONUTF8=1`로 일부 완화), 심볼릭 링크 생성 권한, CRLF 줄바꿈 차이 때문이며 스킬 로직 결함은 아닙니다. 테스트는 모든 스킬의 실제 모델 위임, 모든 실패 복구 경로를 검증하지 않습니다.

실행 경로에 따라 Git·Bash가 필요합니다. Git worktree 대체 절차는 GNU `realpath -m`을 사용하므로 해당 명령이 없는 환경에서는 호스트의 기본 worktree 기능을 우선 사용하세요. 시각적 설계 보조에는 Node.js가, 긴 세션 진단의 일부 경로에는 별도 `context-mode` 도구가 필요할 수 있습니다.

## 사용량 측정

Relay는 검토용 에이전트 생성과 전체 대화 복제를 줄이도록 설계됐습니다. **절감률은 아직 측정되지 않았고 보장되지 않습니다.** Codex는 계정의 7일 창 사용률(`usedPercent`), Claude Code는 플랜 사용량이 비교 지표입니다. 비교하려면 각 기간의 사용률과 수행 작업량, 모델·추론 설정, 재시도와 검증 범위를 함께 기록해야 합니다. 토큰 수나 실행 시간을 한도 절감률로 환산하지 않습니다.

## 이슈·출처

Relay 동작 문제는 [Relay Issues](https://github.com/lsy041015/relay/issues)에 보고하세요.

원본: [Jesse Vincent의 Superpowers](https://github.com/obra/superpowers) 6.4.1. 원본 저작권과 [MIT 라이선스](LICENSE)를 보존했습니다. 원본 설명은 [UPSTREAM_README.md](UPSTREAM_README.md)에 있습니다.
