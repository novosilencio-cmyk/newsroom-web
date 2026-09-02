(function () {
  const exercises = [
    ['Name the anchor', 'Choose one documented detail that gives a reader somewhere to stand. Write it without adding mood, motive or a scene.', 'One sentence and its exact source.', 'Can another reader find the support without asking what you meant?'],
    ['Separate fact and claim', 'Take one institutional statement. Rewrite it so the institution’s verified action and its claimed effect cannot be confused.', 'Two sentences: fact first, attributed claim second.', 'Did any promise quietly become an outcome?'],
    ['Write the unknown', 'Find the most consequential point your source set cannot answer. Make the uncertainty specific enough to report.', 'One uncertainty line and one next-source question.', 'Is the unknown real, or merely a gap you could resolve in the existing source?'],
    ['Find the consequence', 'Replace an abstract policy noun with the decision, resource, obligation, place or routine it may change.', 'A before-and-after pair of sentences.', 'Does the source support the consequence, or only the announced intention?'],
    ['Build a turn', 'Add one sourced limitation or contrasting fact that changes how the opening should be understood.', 'Opening, turn and revised opening—three lines.', 'Does the turn come from evidence rather than manufactured surprise?'],
    ['Mark every carrier', 'Underline each material claim and label who or what carries it: record, source, observation or analysis.', 'A five-claim carrier list.', 'Is any assessment wearing the grammar of a fact?'],
    ['Remove borrowed urgency', 'Take a press-release lead and remove the issuer’s superlatives, inevitability and preferred framing.', 'A 25–40 word independent lead.', 'Is the remaining change still newsworthy? If not, say so.'],
    ['Write a negative control', 'Create the smoothest sentence your sources do not justify, then mark the exact crossing point.', 'The rejected sentence plus a one-line diagnosis.', 'Does your real draft use the same hidden move?'],
    ['Add an overlooked actor', 'Name one person, group or institution that bears a consequence but is absent from the source set.', 'One missing-actor note and one fair question.', 'Are you inferring a view they have not expressed?'],
    ['Test a possible connection', 'Connect two observations, then state what evidence would distinguish a meaningful relationship from coincidence.', 'One hypothesis and one disconfirming test.', 'Can the connection fail without threatening your identity or preferred story?'],
    ['Move from detail to meaning', 'Pair one concrete documented detail with one explanation of why it matters.', 'A two-sentence detail–explanation unit.', 'Does the explanation travel beyond what the detail can carry?'],
    ['Show the limitation', 'Take a promising response or solution and add the strongest relevant boundary: cost, scale, time, access, trade-off or missing evidence.', 'One response sentence and one limitation sentence.', 'Does the limitation inform rather than merely dismiss?'],
    ['Invite constructive disagreement', 'Rewrite a closed conclusion as a bounded claim plus the evidence that would change it.', 'A conclusion and a change-my-mind condition.', 'Could a good-faith critic tell what to test next?'],
    ['Revise by function', 'Read one paragraph three times: first for truth, then movement, then human consequence. Change only one thing per pass.', 'Before, after and three short revision notes.', 'Did fluency improve at the expense of provenance or uncertainty?']
  ];
  const now = new Date();
  const day = Math.floor(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()) / 86400000);
  const index = ((day % exercises.length) + exercises.length) % exercises.length;
  const exercise = exercises[index];
  document.getElementById('daily-date').textContent = now.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }) + ' · UTC';
  document.getElementById('daily-title').textContent = exercise[0];
  document.getElementById('daily-intro').textContent = 'Practice ' + (index + 1) + ' of 14 · one bounded move for the next factual draft.';
  document.getElementById('daily-number').textContent = String(index + 1).padStart(2, '0');
  document.getElementById('daily-task').textContent = exercise[1];
  document.getElementById('daily-deliver').textContent = exercise[2];
  document.getElementById('daily-check').textContent = exercise[3];
}());
