(function () {
  document.querySelectorAll('[data-course-access]').forEach(function (host, index) {
    const preset = host.dataset.course || '';
    const id = 'course-access-' + index;
    host.classList.add('course-access-panel');
    host.innerHTML = '<h2>You can request the full course without joining a mailing list.</h2>' +
      '<p>Complete the two fields and press the button below. Your browser will then ask your device to open its usual email program. A new message will appear with <strong>ai@daena.no</strong> as the recipient and your course choice, reply address and consent choice written into the message.</p>' +
      '<p><strong>The website does not send the message for you.</strong> You must inspect the new email and press Send yourself. If your device has no default email program, write directly to <a class="text-link" href="mailto:ai@daena.no">ai@daena.no</a> and state which course you want. A human must answer and supply the course, so access is not immediate.</p>' +
      '<p class="field-help">Experimental Newsroom keeps access correspondence only as long as it is needed to supply the course and resolve related questions. If you separately request occasional updates, the address is retained until you withdraw that choice by emailing ai@daena.no. You may request deletion through the same address.</p>' +
      '<form class="course-access-form" id="' + id + '">' +
      '<div class="feedback-field"><label for="' + id + '-email">Enter the email address to which the course should be sent. This field is required.</label><input id="' + id + '-email" type="email" autocomplete="email" required></div>' +
      '<div class="feedback-field"><label for="' + id + '-course">Choose the course that you would like to receive. This field is required.</label><select id="' + id + '-course" required><option value="">Choose one</option><option value="Level 1 — Write vividly without inventing">Level 1 — Write vividly without inventing</option><option value="Level 2 — Enter the news through public facts">Level 2 — Enter the news through public facts</option><option value="Levels 1 and 2">Levels 1 and 2</option></select></div>' +
      '<label class="feedback-check"><input id="' + id + '-updates" type="checkbox"><span>This optional choice allows Experimental Newsroom to send me occasional course updates. I understand that I can withdraw it later.</span></label>' +
      '<label class="feedback-check"><input id="' + id + '-privacy" type="checkbox" required><span>I understand that my email address will be used to answer this access request, and I will not include sensitive personal information. This confirmation is required.</span></label>' +
      '<button class="course-action feedback-submit" type="submit">Open the request in my email program →</button>' +
      '<p class="feedback-status" aria-live="polite">Nothing has been sent yet. After the email program opens, review the message and press Send.</p></form>';
    const courseSelect = document.getElementById(id + '-course');
    if (preset) courseSelect.value = preset;
    const form = document.getElementById(id);
    const status = form.querySelector('.feedback-status');
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const email = document.getElementById(id + '-email').value.trim();
      const course = courseSelect.value;
      const updates = document.getElementById(id + '-updates').checked;
      const subject = 'Free course access request — ' + course;
      const body = ['COURSE ACCESS REQUEST', 'Course: ' + course, 'Reply-to email: ' + email, 'Requested at: ' + new Date().toISOString(), 'Course updates consent: ' + (updates ? 'Yes — optional consent given; I may withdraw at any time' : 'No'), '', 'Please use my email address to answer this access request. I understand that a human reply is required.', 'I have not included sensitive personal information.'].join('\n');
      status.textContent = 'Your device is being asked to open a new email. Nothing is sent until you press Send in the email program.';
      window.location.href = 'mailto:ai@daena.no?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  });
}());
