(function () {
  const destination = 'ai@daena.no';

  function field(name, label, options) {
    const wrapper = document.createElement('div');
    wrapper.className = 'feedback-field';
    const labelElement = document.createElement('label');
    labelElement.setAttribute('for', name);
    labelElement.textContent = label;
    wrapper.appendChild(labelElement);

    let control;
    if (options.type === 'textarea') {
      control = document.createElement('textarea');
      control.rows = options.rows || 5;
      control.maxLength = options.maxLength || 1800;
    } else if (options.type === 'select') {
      control = document.createElement('select');
      options.values.forEach(function (value) {
        const option = document.createElement('option');
        option.value = value[0];
        option.textContent = value[1];
        control.appendChild(option);
      });
    } else {
      control = document.createElement('input');
      control.type = options.type || 'text';
      if (options.maxLength) control.maxLength = options.maxLength;
    }
    control.id = name;
    control.name = name;
    if (options.required) control.required = true;
    if (options.placeholder) control.placeholder = options.placeholder;
    wrapper.appendChild(control);
    if (options.help) {
      const help = document.createElement('p');
      help.className = 'field-help';
      help.textContent = options.help;
      wrapper.appendChild(help);
    }
    return wrapper;
  }

  document.querySelectorAll('[data-feedback-form]').forEach(function (host, index) {
    const kind = host.dataset.feedbackKind || 'Publication';
    const title = host.dataset.feedbackTitle || document.title;
    const publicationId = host.dataset.feedbackId || window.location.pathname;
    const formId = 'editorial-feedback-' + index;

    host.innerHTML = '';
    host.classList.add('feedback-panel');
    const heading = document.createElement('h2');
    heading.textContent = 'Add what we may have missed';
    host.appendChild(heading);
    const introduction = document.createElement('p');
    introduction.textContent = 'Send a correction, source, new angle, possible connection, limitation or course improvement. Required fields are marked. The website does not store your answers; it prepares an email for you to review and send.';
    host.appendChild(introduction);

    const form = document.createElement('form');
    form.id = formId;
    form.className = 'feedback-form';
    form.appendChild(field(formId + '-type', 'Contribution type — required', {
      type: 'select', required: true, values: [
        ['', 'Choose one'],
        ['Correction', 'Correction'],
        ['Source or evidence', 'Source or evidence'],
        ['New angle or overlooked actor', 'New angle or overlooked actor'],
        ['Possible connection', 'Possible connection'],
        ['Response or alternative', 'Response or alternative'],
        ['Limitation or risk', 'Limitation or risk'],
        ['Course improvement', 'Course improvement'],
        ['Comment or question', 'Comment or question']
      ]
    }));
    form.appendChild(field(formId + '-status', 'What status best describes it? — required', {
      type: 'select', required: true, values: [
        ['', 'Choose one'],
        ['Directly observed', 'Directly observed'],
        ['Supported by a source', 'Supported by a source'],
        ['Reasoned hypothesis', 'Reasoned hypothesis'],
        ['Open question', 'Open question'],
        ['Personal experience', 'Personal experience']
      ]
    }));
    form.appendChild(field(formId + '-message', 'Your contribution — required', {
      type: 'textarea', required: true, rows: 7, maxLength: 2400,
      placeholder: 'State the point, why it matters, and what could test or improve it.'
    }));
    form.appendChild(field(formId + '-source', 'Source link or reference — optional', {
      type: 'url', maxLength: 600, placeholder: 'https://…',
      help: 'For personal observations, say when and where in the contribution instead. Do not include private or sensitive information.'
    }));
    form.appendChild(field(formId + '-credit', 'How may we credit you? — optional', {
      type: 'text', maxLength: 160,
      placeholder: 'Name, organisation, “anonymous”, or leave blank'
    }));

    const permission = document.createElement('label');
    permission.className = 'feedback-check';
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.required = true;
    permission.appendChild(checkbox);
    const permissionText = document.createElement('span');
    permissionText.textContent = 'Required: I understand this is an editorial submission, not private correspondence. It may be checked, edited or declined; it will not become an OØS finding or publication without source, harm, privacy and relevance review.';
    permission.appendChild(permissionText);
    form.appendChild(permission);

    const button = document.createElement('button');
    button.type = 'submit';
    button.className = 'course-action feedback-submit';
    button.textContent = 'Prepare email →';
    form.appendChild(button);
    const status = document.createElement('p');
    status.className = 'feedback-status';
    status.setAttribute('aria-live', 'polite');
    status.textContent = 'Your email app will open. You can inspect and change the message before sending.';
    form.appendChild(status);
    host.appendChild(form);

    const review = document.createElement('details');
    review.className = 'review-gate';
    review.innerHTML = '<summary>How submissions are evaluated</summary><p>We check factual change, source strength, testability, overlooked people or consequences, privacy and harm, duplication, and likely public or OØS value. A submission may be classified as <strong>correct</strong>, <strong>test</strong>, <strong>develop</strong>, <strong>hold</strong> or <strong>no action</strong>. Useful material may be clarified or combined, but uncertainty and origin should remain visible.</p>';
    host.appendChild(review);

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const get = function (suffix) { return document.getElementById(formId + suffix).value.trim(); };
      const type = get('-type');
      const evidenceStatus = get('-status');
      const message = get('-message');
      const source = get('-source');
      const credit = get('-credit');
      const subject = '[Editorial submission] ' + kind + ' · ' + type + ' · ' + publicationId;
      const lines = [
        'PUBLICATION',
        'Kind: ' + kind,
        'Title: ' + title,
        'ID: ' + publicationId,
        'URL: ' + window.location.href,
        '',
        'SUBMISSION',
        'Type: ' + type,
        'Status claimed: ' + evidenceStatus,
        'Credit preference: ' + (credit || 'Not stated'),
        'Source or reference: ' + (source || 'Not supplied'),
        '',
        message,
        '',
        'I understand that this is an editorial submission and that review is required before any use.'
      ];
      status.textContent = 'Opening your email app. Review the message before sending.';
      window.location.href = 'mailto:' + destination + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
    });
  });
}());
