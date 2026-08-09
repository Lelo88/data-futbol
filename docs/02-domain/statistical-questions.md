# Statistical Questions

## Purpose

This document defines the statistical questions Data-Futbol should be able to answer without prescribing implementation details.

## 1. Recent Form

- How many of the last N official matches were wins, draws, or losses?
- What are the win, draw, and loss percentages?
- How many goals were scored and conceded?
- What are the average goals scored and conceded?
- How many clean sheets occurred?
- In how many matches did the team concede?
- What is the current result sequence?

Supported scopes:
- All official competitions
- Specific competition
- Overall
- Home
- Away

N is configurable, with 10 as the primary use case.

## 2. Results

- How many matches were won, drawn, or lost?
- What is the win/draw/loss distribution?
- How does it differ between home and away?
- How does it differ by competition?
- How does it change with sample size?

## 3. Goals

- How many goals were scored?
- How many were conceded?
- What are the average goals scored and conceded?
- What is the average total goals per match?
- How often did the team score?
- How often did it concede?
- How often did matches exceed a selected goals line?
- How often did matches remain below it?

Specific market lines depend on source availability.

## 4. Home and Away

- How does performance differ overall, at home, and away?
- How do win/draw/loss rates change?
- How do goals scored and conceded change?
- How do cards change?
- How do market-related frequencies change?

## 5. League Position

When standings are available:
- What is the team's position?
- How many matches has it played?
- How many wins, draws, and losses?
- How many goals for and against?
- What is the goal difference?
- How many points?
- What was the position at the relevant point in the season?

## 6. Cards

- How many yellow cards were received?
- How many red cards?
- What are average total, yellow, and red cards?
- How often did the team receive more cards than its opponent?
- How do card statistics differ home/away and by competition?

For matches:
- Total cards
- Total yellow cards
- Total red cards
- Which team received more cards?

## 7. Head-to-Head

For two teams:
- How many of the last N official H2H matches were won by each team?
- How many were draws?
- How many goals were scored by each team?
- What is the average total goals?
- How many yellow and red cards were recorded?
- Which team received more cards?
- How do results differ by competition and home/away context?

H2H is independent from recent form.

## 8. 1X2

- How often did the home team win?
- How often was the match a draw?
- How often did the away team win?
- How do frequencies change by sample, competition, and context?
- How do historical frequencies compare with opening odds?

## 9. Double Chance

- How often did 1X occur?
- How often did X2 occur?
- How often did 12 occur?
- How do frequencies change by sample and competition?
- How do historical frequencies compare with opening odds?

## 10. Goals Over/Under

For a selected line:
- How often did Over occur?
- How often did Under occur?
- How do frequencies differ by team, home/away, competition, and H2H?
- How do historical frequencies compare with opening odds?

## 11. Most Cards

- How often did the home team receive more cards?
- How often did the away team receive more cards?
- How often was the card count equal?
- How do frequencies change by competition and context?
- How do H2H frequencies compare?
- How do historical frequencies compare with opening odds?

## 12. Cards Over/Under

For a selected line:
- How often did Over occur?
- How often did Under occur?
- What is the average total cards?
- How does it vary by competition, teams, and H2H?
- How do historical frequencies compare with opening odds?

## 13. Opening Odds

For a market selection:
- What was the opening odds value?
- Which bookmaker provided it?
- Which market and selection did it represent?
- What implied probability does it represent?
- How does it compare with historical statistical frequency?

Closing odds are outside the initial MVP.

## 14. Cross-Team Analysis

For two teams:
- Which has better recent form?
- Which scores more?
- Which concedes fewer?
- Which performs better in the relevant home/away context?
- Which receives more cards?
- What does H2H indicate?
- What are their league positions?
- How do statistical profiles compare with opening odds?
- Are there meaningful differences between recent form and H2H?
- Are there relationships not visible from a single metric?

## 15. Insights

Insights must be derived from measurable statistical evidence.

Examples:
- Team A has stronger recent win rate than Team B.
- Team B has conceded fewer goals over the selected sample.
- H2H is more balanced than recent form suggests.
- Team A receives significantly more cards.
- Historical market frequency differs from implied opening probability.

The underlying evidence and analysis scope must be identifiable.

## 16. Statistical Context

Every statistical result should retain enough context to understand it, including:
- Team
- Opponent when applicable
- Competition scope
- Sample size
- Match period
- Home/away scope
- H2H scope when applicable
- Market and line when applicable

A statistic without context should not be treated as directly comparable to another statistic.
