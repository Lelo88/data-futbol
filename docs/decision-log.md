## 2026-08

### Restart the project from scratch

- Date: 2026-08
- Decision: The project was restarted from scratch.
- Reason: The project direction changed after evaluating the real problem and shifting from a backend-oriented scope to a historical football analytics platform.
- Consequences:
	- The previous direction was discarded.
	- The project is being rebuilt around documentation-first foundations.

### Python replacing Go

- Date: 2026-08
- Decision: Python became the preferred primary language instead of Go.
- Reason: Python offers a richer ecosystem for data analytics.
- Consequences:
	- Pandas becomes the primary analysis library.
	- SQLAlchemy replaces GORM.
	- Clean Architecture remains as a design principle, adapted to Python.

### Historical data instead of real-time data

- Date: 2026-08
- Decision: The project will use historical football data rather than real-time data.
- Reason: The platform is focused on historical statistics and decision support, and live data ingestion was removed from the current direction.
- Consequences:
	- Live match data is excluded from the MVP.
	- Live odds are excluded from the MVP.
	- Analysis is centered on historical evidence.

### No AI predictions in the MVP

- Date: 2026-08
- Decision: AI-based predictions are not part of the MVP.
- Reason: The platform is intended to support decision-making through statistical evidence rather than predictions.
- Consequences:
	- AI predictions remain outside the initial scope.
	- Automatic betting and real-time recommendations are excluded from the MVP.

### Official matches only

- Date: 2026-08
- Decision: Only official matches are valid for MVP statistics.
- Reason: The domain defines official matches as the only valid source for historical analysis.
- Consequences:
	- All competitions means all available official competitions.
	- Invalid, cancelled, abandoned, annulled, or otherwise non-eligible matches are excluded.

### Friendly matches excluded

- Date: 2026-08
- Decision: Friendly, preseason, exhibition, and other non-official matches are excluded.
- Reason: The domain explicitly excludes non-official fixtures from MVP statistics.
- Consequences:
	- Friendly matches do not enter recent form, goals, results, cards, standings, H2H, market analysis, or insight generation.

### Configurable last N matches

- Date: 2026-08
- Decision: Recent match analysis uses a configurable sample size of the last N eligible official matches.
- Reason: The domain and statistical questions documents define N as configurable, with 10 as the primary use case.
- Consequences:
	- Recent form calculations support different sample sizes.
	- The default use case is 10 matches.

### H2H as an independent analytical context

- Date: 2026-08
- Decision: Head-to-head is treated as an independent analytical context.
- Reason: H2H must not be silently merged into recent-form statistics.
- Consequences:
	- H2H is analyzed separately from recent form.
	- H2H retains its own scope, sample, and context.

### Statistical result based on regular time

- Date: 2026-08
- Decision: The MVP statistical result is based on the score at the end of regular time.
- Reason: The domain distinguishes regular time from the final outcome.
- Consequences:
	- A match level after regular time remains a draw statistically, even if extra time produces a winner.
	- Regular-time and final outcomes are not conflated.

### Extra time and penalty shootouts stored separately

- Date: 2026-08
- Decision: Extra-time information and penalty-shootout information are stored separately.
- Reason: The domain preserves regular-time score, final score after extra time, and penalty-shootout result as distinct match context.
- Consequences:
	- Extra time does not replace the regular-time statistical result.
	- Penalty-shootout outcomes remain separate from the main match result.

### Penalty shootout goals not counted as match goals

- Date: 2026-08
- Decision: Penalty-shootout goals are not counted as match goals.
- Reason: The domain explicitly excludes penalty-kick goals from match goals.
- Consequences:
	- Goal statistics remain based on in-match scoring.
	- Shootout scoring is tracked separately from match scoring.

### Opening odds as the primary odds target

- Date: 2026-08
- Decision: Opening odds are the primary odds target for the MVP.
- Reason: The domain defines opening odds as the earliest recorded bookmaker odds and the main target for the MVP.
- Consequences:
	- Closing odds are outside the initial MVP.
	- Odds records may include match, market, selection, bookmaker, and opening odds.

### MVP markets

- Date: 2026-08
- Decision: The MVP markets are 1X2, Double Chance, Goals Over/Under, Most Cards, and Cards Over/Under.
- Reason: These markets are explicitly defined in the domain and glossary, while BTTS is postponed until after the MVP.
- Consequences:
	- Market analysis in the MVP is limited to these selections.
	- Specific lines depend on source availability and will be validated against real historical sources before implementation.

### BTTS postponed until after the MVP

- Date: 2026-08
- Decision: Both Teams To Score is postponed until after the MVP.
- Reason: BTTS is defined as a post-MVP market in the domain documentation.
- Consequences:
	- BTTS is not included in the initial MVP scope.
	- BTTS may be considered in a future version.