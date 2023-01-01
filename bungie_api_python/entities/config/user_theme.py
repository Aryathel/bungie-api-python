from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True)
class UserTheme:
    userThemeId: int
    userThemeName: str
    userThemeDescription: str
