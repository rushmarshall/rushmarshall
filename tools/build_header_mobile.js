// Animated GitHub header: real streamlines traced through the same noise field the website's header uses.
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const d=__dirname;const W=640,H=380;
// --- text layer (site fonts) as a transparent PNG ---
const b=await chromium.launch();const p=await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:2});
await p.goto('file://'+d+'/text_mobile.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
const png=await (await p.$('#t')).screenshot({omitBackground:true});await b.close();
// --- the site's field (same constants as index.html flowField) ---
function hash3(i,j,k){let n=(i*374761393+j*668265263+k*1442695040)|0;n=(n^(n>>13))|0;n=(n*1274126177)|0;n=(n^(n>>16))|0;return((n>>>0)%100000)/100000;}
const fade=a=>a*a*a*(a*(a*6-15)+10),lerp=(a,b,m)=>a+(b-a)*m;
function vnoise(x,y,z){const xi=Math.floor(x),yi=Math.floor(y),zi=Math.floor(z),xf=x-xi,yf=y-yi,zf=z-zi,u=fade(xf),v=fade(yf),w=fade(zf);const c=(a,b,c2)=>hash3(xi+a,yi+b,zi+c2);const x00=lerp(c(0,0,0),c(1,0,0),u),x10=lerp(c(0,1,0),c(1,1,0),u),x01=lerp(c(0,0,1),c(1,0,1),u),x11=lerp(c(0,1,1),c(1,1,1),u);return lerp(lerp(x00,x10,v),lerp(x01,x11,v),w);}
const S=0.0016,EPS=1.4,SPEED=1.4,T=0.2;
const pot=(x,y)=>vnoise(x*S,y*S,T)+0.5*vnoise(x*S*2.3+31.4,y*S*2.3-12.7,T*1.35+5.0);
function dir(x,y){const dy=pot(x,y+EPS)-pot(x,y-EPS),dx=pot(x+EPS,y)-pot(x-EPS,y);let vx=dy,vy=-dx;const m=Math.hypot(vx,vy)||1e-6;return [vx/m,vy/m];}
let seed=20261112;const rnd=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
const SC=2.1; // the header is a small window: sample the field at site scale so eddies look like the site's
const CL=[70,154,182],CH=[150,232,240];let defs='',stat='',mov='';const N=250;
for(let i=0;i<N;i++){let x=rnd()*W,y=rnd()*H;const steps=120+Math.floor(rnd()*200);const pts=[];
 for(let s=0;s<steps;s++){if(s%4===0)pts.push(x.toFixed(1)+' '+y.toFixed(1));const v=dir(x*SC,y*SC);x+=v[0]*SPEED;y+=v[1]*SPEED;if(x<-20||x>W+20||y<-20||y>H+20)break;}
 if(pts.length<6)continue;const mix=Math.pow(rnd(),1.7),c=CL.map((l,k)=>Math.round(lerp(l,CH[k],mix)));
 defs+=`<path id="l${i}" pathLength="100" d="M${pts.join('L')}"/>`;
 const col=`rgb(${c.join(',')})`,w=(0.7+mix*0.7).toFixed(2);
 stat+=`<use href="#l${i}" stroke="${col}" stroke-width="${w}" opacity="${(0.16+mix*0.2).toFixed(2)}"/>`;
 mov+=`<use href="#l${i}" class="m" stroke="${col}" stroke-width="${(+w+0.25).toFixed(2)}" opacity="${(0.5+mix*0.4).toFixed(2)}" style="animation-duration:${(7+rnd()*9).toFixed(1)}s;animation-delay:-${(rnd()*16).toFixed(1)}s"/>`;}
const svg=`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Sebastian R.O. Marshall, Climate Scientist and Ph.D. Researcher, Johns Hopkins University">
<defs><radialGradient id="bg" cx="50%" cy="0%" r="120%"><stop offset="0" stop-color="#0a2a3b"/><stop offset=".42" stop-color="#06212f"/><stop offset="1" stop-color="#03101a"/></radialGradient>
<radialGradient id="vig" cx="50%" cy="45%" r="70%"><stop offset=".4" stop-color="#03101a" stop-opacity="0"/><stop offset="1" stop-color="#03101a" stop-opacity=".55"/></radialGradient>
<radialGradient id="back" cx="50%" cy="50%" r="50%" gradientTransform="translate(0.5 0.5) scale(0.92 1.24) translate(-0.5 -0.5)"><stop offset="0" stop-color="#03101a" stop-opacity=".8"/><stop offset=".55" stop-color="#03101a" stop-opacity=".5"/><stop offset="1" stop-color="#03101a" stop-opacity="0"/></radialGradient>
<clipPath id="card"><rect width="${W}" height="${H}" rx="26"/></clipPath>
<style>use{fill:none;stroke-linecap:round}.m{stroke-dasharray:34 66;animation:flow 10s linear infinite}@keyframes flow{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}@media (prefers-reduced-motion:reduce){.m{animation:none}}</style>
<g fill="none">${defs}</g></defs>
<g clip-path="url(#card)"><rect width="${W}" height="${H}" fill="url(#bg)"/><g>${stat}</g><g>${mov}</g><rect width="${W}" height="${H}" fill="url(#vig)"/><rect width="${W}" height="${H}" fill="url(#back)"/>
<image width="${W}" height="${H}" href="data:image/png;base64,${png.toString('base64')}"/></g>
<rect x=".5" y=".5" width="${W-1}" height="${H-1}" rx="26" fill="none" stroke="#e9f6fc" stroke-opacity=".14"/></svg>`;
fs.writeFileSync(d+'/header-mobile.svg',svg);console.log('header-mobile.svg',(svg.length/1024).toFixed(0)+' KB','text layer',(png.length/1024).toFixed(0)+' KB');
})();
