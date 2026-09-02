(function () {
  document.querySelectorAll('[data-course-access]').forEach(function (host, index) {
    const preset = host.dataset.course || '';
    const id = 'course-access-' + index;
    host.classList.add('course-access-panel');
    host.innerHTML = '<h2>Request free access</h2>' +
      '<p>Tell us where to send the course. This website does not transmit or store the form: submitting opens a prepared message in your email app. A human reply is required, so access is not instant.</p>' +
      '<p class="field-help">Access correspondence is kept only as long as needed to deliver the course and resolve related follow-up. If you separately request updates, the address is retained until you withdraw by emailing ai@daena.no. You may request deletion through the same address.</p>' +
      '<form class="course-access-form" id="' + id + '">' +
      '<div class="feedback-field"><label for="' + id + '-email">Your email address — required</label><input id="' + id + '-email" type="email" autocomplete="email" required></div>' +
      '<div class="feedback-field"><label for="' + id + '-course">Course — required</label><select id="' + id + '-course" required><option value="">Choose one</option><option value="Level 1 — Write vividly without inventing">Level 1 — Write vividly without inventing</option><option value="Level 2 — Enter the news through public facts">Level 2 — Enter the news through public facts</option><option value="Levels 1 and 2">Levels 1 and 2</option></select></div>' +
      '<label class="feedback-check"><input id="' + id + '-updates" type="checkbox"><span>Optional: I would also like occasional course updates. This is separate from receiving the course and may be withdrawn.</span></label>' +
      '<label class="feedback-check"><input id="' + id + '-privacy" type="checkbox" required><span>Required: I understand that my email will be used to answer this access request. I will not include sensitive personal information.</span></label>' +
      '<button class="course-action feedback-submit" type="submit">Prepare access email →</button>' +
      '<p class="feedback-status" aria-live="polite">You can inspect and change the message before sending.</p></form>';
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
      status.textContent = 'Opening your email app. Send the message to complete the request.';
      window.location.href = 'mailto:ai@daena.no?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  });
}());
