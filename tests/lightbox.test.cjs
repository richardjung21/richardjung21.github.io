const {test}=require('node:test');
const assert=require('node:assert/strict');
const {readFileSync}=require('node:fs');
const {join}=require('node:path');
const {runInNewContext}=require('node:vm');
function setup(reduced=false,available=true){
 const options=[];let clicked=0;
 const motion={matches:reduced,addEventListener(n,f){this.change=f;}};
 const link={addEventListener(n,f){this.click=f;},closest(){return {querySelector(){return {click(){clicked++;}};}};}};
 const window={matchMedia:()=>motion,jQuery:{fx:{off:false}}};
 if(available)window.lightbox={option:o=>options.push(o)};
 const document={addEventListener(n,f){f();},querySelectorAll:()=>[link]};
 runInNewContext(readFileSync(join(__dirname,'..','lightbox.js'),'utf8'),{window,document});
 return {options,motion,window,link,clicked:()=>clicked};
}
test('upstream animation timings and safe captions are configured',()=>{
 const u=setup();assert.equal(u.options[0].fadeDuration,600);assert.equal(u.options[0].imageFadeDuration,600);
 assert.equal(u.options[0].resizeDuration,700);assert.equal(u.options[0].sanitizeTitle,true);
 assert.equal(u.options[0].disableScrolling,true);
});
test('reduced motion disables all library animations and can be changed live',()=>{
 const u=setup(true);assert.equal(u.options[0].resizeDuration,0);assert.equal(u.window.jQuery.fx.off,true);
 u.motion.matches=false;u.motion.change();assert.equal(u.options[1].fadeDuration,600);assert.equal(u.window.jQuery.fx.off,false);
});
test('caption link opens the existing image entry and preserves modified gestures',()=>{
 const u=setup();let prevented=false;u.link.click({button:0,preventDefault(){prevented=true;}});
 assert.equal(prevented,true);assert.equal(u.clicked(),1);
 u.link.click({button:0,ctrlKey:true});assert.equal(u.clicked(),1);
 assert.equal(setup(false,false).link.click,undefined);
});
