class CheckSummaryPresenter:
    def render(self, files_found: int, files_excluded: int, files_checked: int) -> str:
        return "\n".join(
            [
                "Check Summary:",
                f"- Files found in scope: {files_found}",
                f"- Files excluded by rules: {files_excluded}",
                f"- Files checked: {files_checked}",
            ]
        )
