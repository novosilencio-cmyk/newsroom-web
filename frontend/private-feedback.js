/* Inactive adapter: it loads no external service until an endpoint/widget is configured. */
(function(root) {
  'use strict';
  async function submit(endpoint, payload, send) {
    const response = await send(endpoint, {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload), credentials:'omit', cache:'no-store'
    });
    const receipt = await response.json();
    if (!response.ok || receipt.status !== 'stored_privately' ||
        typeof receipt.receipt_id !== 'string' || receipt.receipt_id !== payload.request_id) {
      throw new Error('No confirmed receipt');
    }
    return receipt;
  }
  function mount(host, options) {
    const labels = options.labels;
    host.replaceChildren();
    function element(tag, text) { const e=document.createElement(tag); if (text) e.textContent=text; return e; }
    const title=element('h2',labels[2]); host.append(title);
    const form=element('form'); host.append(form);
    const id='private-feedback-'+crypto.randomUUID();
    function field(tag, suffix, labelText) {
      const label=element('label',labelText); const input=element(tag);
      input.id=id+suffix; label.htmlFor=input.id; form.append(label,input); return input;
    }
    const message=field('textarea','-message',labels[3]); message.rows=6; message.required=true; message.maxLength=4000;
    const email=field('input','-email',labels[4]); email.type='email'; email.maxLength=254;
    const widget=element('div'); form.append(widget);
    const button=element('button',labels[5]); button.type='submit'; form.append(button);
    const status=element('p'); status.setAttribute('role','status'); status.setAttribute('aria-live','polite'); form.append(status);
    const text=options.statusText;
    const requestId=crypto.randomUUID(); let widgetId, pending=false;
    const endpoint=options.endpoint ? new URL(options.endpoint,location.href) : null;
    const configured=endpoint && endpoint.protocol==='https:' && options.siteKey && root.turnstile;
    button.disabled=!configured;
    status.textContent=configured ? text.privateNotice : text.unavailable;
    if (configured) widgetId=root.turnstile.render(widget,{sitekey:options.siteKey,action:'private-feedback'});
    form.addEventListener('submit',async function(event) {
      event.preventDefault(); if (!configured || pending || !form.reportValidity()) return;
      const token=root.turnstile.getResponse(widgetId);
      if (!token) { status.textContent=text.verificationNeeded; return; }
      pending=true; button.disabled=true; status.textContent=text.sending;
      try {
        const receipt=await submit(endpoint.href,{
          request_id:requestId, article_id:options.articleId, text:message.value,
          reply_email:email.value, language:options.language || 'nb', anti_spam_token:token, visibility:'private'
        },root.fetch.bind(root));
        status.textContent=text.received+' '+receipt.receipt_id;
        message.value=''; email.value='';
        // Keep successful form closed; retrying a failed request keeps the same id.
      } catch(error) {
        status.textContent=text.failed; button.disabled=false;
        root.turnstile.reset(widgetId); // expired/single-use token needs refreshing
      } finally { pending=false; }
    });
    return {configured:Boolean(configured)};
  }
  const api={submit,mount};
  if (typeof module!=='undefined' && module.exports) module.exports=api;
  else root.ExpNRPrivateFeedback=api;
})(typeof window!=='undefined' ? window : globalThis);
