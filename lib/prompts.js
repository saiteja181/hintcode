const Prompts = {
  _systemPrompt: `You are HintCode, a sharp coding mentor who reads students' code carefully. Rules:
- Be concise. No filler, no fluff, no "great effort" praise.
- Never start with "I can see" or "It looks like" or similar padding.
- Always analyze the student's actual code. Quote the specific line or variable that has the bug.
- Explain WHY that specific part fails by giving a concrete failing input/case.
- Talk to the student directly using "you/your".
- Use plain text only. No markdown, no bullet points, no numbered lists.`,

  _buildCodeContext(userCode, language) {
    if (!userCode || !userCode.trim()) {
      return '\n[No code written yet]';
    }
    const lines = userCode.split('\n');
    const numbered = lines.map((line, i) => `Line ${i + 1}: ${line}`).join('\n');
    return `\nStudent's code (${language}) with line numbers:\n${numbered}`;
  },

  buildHintPrompt(level, problemTitle, problemStatement, userCode, language) {
    const codeSection = this._buildCodeContext(userCode, language);
    const hasCode = userCode && userCode.trim().length > 0;
    const context = `Problem: "${problemTitle}"\n${problemStatement}${codeSection}`;

    switch (level) {
      case HINT_LEVELS.NUDGE:
        return [
          { role: 'system', content: this._systemPrompt },
          {
            role: 'user',
            content: `${context}

Give a GENTLE NUDGE in 2-3 short sentences.
${hasCode
  ? `- Look at their code. Find the FIRST line where the logic will produce a wrong answer.
- Quote that line (e.g. "Your line 4: m = 0 ...").
- Ask them: "What happens when [specific failing input]?" to make them see the bug themselves.
- Do NOT name the fix, the algorithm, or the correct approach.`
  : `- Ask ONE pointed question about a tricky case in this problem.
- Make them think about an input where the obvious approach fails.
- Do NOT name any algorithm or technique.`}`,
          },
        ];

      case HINT_LEVELS.APPROACH:
        return [
          { role: 'system', content: this._systemPrompt },
          {
            role: 'user',
            content: `${context}

Give an APPROACH HINT in 3-4 short sentences.
${hasCode
  ? `- First, quote the exact line(s) causing the bug and explain WHY it fails with a specific input.
- Then name the technique or data structure that fixes this.
- Do NOT give the fix or corrected code. Just name what to use and why their current logic breaks.`
  : `- Name the technique or data structure that solves this problem.
- Give ONE concrete observation about the problem that connects to this technique.
- Do NOT explain how to implement it.`}`,
          },
        ];

      case HINT_LEVELS.DETAILED:
        return [
          { role: 'system', content: this._systemPrompt },
          {
            role: 'user',
            content: `${context}

Give a DETAILED GUIDE in 5-7 short sentences.
${hasCode
  ? `- Quote every line that has a bug or missing logic. For each, explain what goes wrong and with what input.
- Then describe the correct approach step-by-step in plain English.
- Mention 1-2 edge cases their code does not handle (e.g. all negatives, single element, empty array).
- Do NOT write corrected code. Describe what each step should do so they can fix it themselves.`
  : `- Lay out the optimal approach as a sequence of plain-English steps.
- Mention 1-2 edge cases to watch for.
- Do NOT write any code or pseudocode.`}`,
          },
        ];

      case HINT_LEVELS.SOLUTION:
        return [
          { role: 'system', content: this._systemPrompt.replace(
            'Use plain text only. No markdown, no bullet points, no numbered lists.',
            'You may use code blocks for the solution code.'
          )},
          {
            role: 'user',
            content: `${context}

Provide the FULL SOLUTION in this exact structure:

BUG: ${hasCode ? 'Quote the buggy line(s) from their code. For each, explain what input breaks it and why.' : 'Skip this section.'}

APPROACH: 2-3 sentences explaining the core insight of the optimal solution.

SOLUTION:
Write the complete corrected code in ${language || 'Python'}. Add a short inline comment on any line that was changed/fixed from the student's version.

COMPLEXITY: Time and space in one line.

TAKEAWAY: One sentence — the pattern to remember for similar problems.

Under 250 words total. No repetition. No restating the problem.`,
          },
        ];

      default:
        throw new Error(`Invalid hint level: ${level}`);
    }
  },
};
