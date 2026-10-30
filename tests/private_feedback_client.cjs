const assert=require('node:assert/strict');
const {submit}=require('../frontend/private-feedback.js');
(async()=>{
  const payload={request_id:'request-1',text:'Keep this until actual receipt'};
  const ok=async()=>({ok:true,json:async()=>({status:'stored_privately',receipt_id:'request-1'})});
  assert.equal((await submit('https://intake.example/feedback',payload,ok)).receipt_id,'request-1');
  for (const receipt of [{status:'queued',receipt_id:'request-1'}, {status:'stored_privately',receipt_id:'wrong'}, {status:'stored_privately'}]) {
    await assert.rejects(submit('https://intake.example/feedback',payload,async()=>({ok:true,json:async()=>receipt})));
  }
  await assert.rejects(submit('https://intake.example/feedback',payload,async()=>({ok:false,json:async()=>({status:'stored_privately',receipt_id:'request-1'})})));
  await assert.rejects(submit('https://intake.example/feedback',payload,async()=>{throw Error('network failure')}));
  assert.equal(payload.text,'Keep this until actual receipt');
  console.log('PASS: receipt validation, HTTP/network failures and original message retained');
})().catch(e=>{console.error(e);process.exit(1)});
