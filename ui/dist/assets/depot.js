import{ar as I,as as F,y as N}from"./main.js";import{N as P}from"./headers.js";import{as as h,au as f,ar as b,B as V,ax as H,ay as B,b0 as L,j as A,aA as M,H as a,F as S,r as T,s as W,bs as m,bC as C,bv as o,bu as l,b3 as q,k as _,bE as y,bD as z,bo as G,bx as J,bt as R}from"./_plugin-vue_export-helper.js";import{b as K,_ as Q}from"./Grid.js";import{_ as U}from"./Divider.js";import{_ as X}from"./Avatar.js";import"./get-slot.js";import"./Tag.js";const Y=h("thing",`
 display: flex;
 transition: color .3s var(--n-bezier);
 font-size: var(--n-font-size);
 color: var(--n-text-color);
`,[h("thing-avatar",`
 margin-right: 12px;
 margin-top: 2px;
 `),h("thing-avatar-header-wrapper",`
 display: flex;
 flex-wrap: nowrap;
 `,[h("thing-header-wrapper",`
 flex: 1;
 `)]),h("thing-main",`
 flex-grow: 1;
 `,[h("thing-header",`
 display: flex;
 margin-bottom: 4px;
 justify-content: space-between;
 align-items: center;
 `,[f("title",`
 font-size: 16px;
 font-weight: var(--n-title-font-weight);
 transition: color .3s var(--n-bezier);
 color: var(--n-title-text-color);
 `)]),f("description",[b("&:not(:last-child)",`
 margin-bottom: 4px;
 `)]),f("content",[b("&:not(:first-child)",`
 margin-top: 12px;
 `)]),f("footer",[b("&:not(:first-child)",`
 margin-top: 12px;
 `)]),f("action",[b("&:not(:first-child)",`
 margin-top: 12px;
 `)])])]),Z=Object.assign(Object.assign({},B.props),{title:String,titleExtra:String,description:String,descriptionClass:String,descriptionStyle:[String,Object],content:String,contentClass:String,contentStyle:[String,Object],contentIndented:Boolean}),ee=V({name:"Thing",props:Z,setup(t,{slots:e}){const{mergedClsPrefixRef:g,inlineThemeDisabled:d,mergedRtlRef:s}=H(t),$=B("Thing","-thing",Y,I,t,g),v=L("Thing",s,g),p=A(()=>{const{self:{titleTextColor:u,textColor:n,titleFontWeight:r,fontSize:c},common:{cubicBezierEaseInOut:w}}=$.value;return{"--n-bezier":w,"--n-font-size":c,"--n-text-color":n,"--n-title-font-weight":r,"--n-title-text-color":u}}),i=d?M("thing",void 0,p,t):void 0;return()=>{var u;const{value:n}=g,r=v?v.value:!1;return(u=i==null?void 0:i.onRender)===null||u===void 0||u.call(i),a("div",{class:[`${n}-thing`,i==null?void 0:i.themeClass,r&&`${n}-thing--rtl`],style:d?void 0:p.value},e.avatar&&t.contentIndented?a("div",{class:`${n}-thing-avatar`},e.avatar()):null,a("div",{class:`${n}-thing-main`},!t.contentIndented&&(e.header||t.title||e["header-extra"]||t.titleExtra||e.avatar)?a("div",{class:`${n}-thing-avatar-header-wrapper`},e.avatar?a("div",{class:`${n}-thing-avatar`},e.avatar()):null,e.header||t.title||e["header-extra"]||t.titleExtra?a("div",{class:`${n}-thing-header-wrapper`},a("div",{class:`${n}-thing-header`},e.header||t.title?a("div",{class:`${n}-thing-header__title`},e.header?e.header():t.title):null,e["header-extra"]||t.titleExtra?a("div",{class:`${n}-thing-header__extra`},e["header-extra"]?e["header-extra"]():t.titleExtra):null),e.description||t.description?a("div",{class:[`${n}-thing-main__description`,t.descriptionClass],style:t.descriptionStyle},e.description?e.description():t.description):null):null):a(S,null,e.header||t.title||e["header-extra"]||t.titleExtra?a("div",{class:`${n}-thing-header`},e.header||t.title?a("div",{class:`${n}-thing-header__title`},e.header?e.header():t.title):null,e["header-extra"]||t.titleExtra?a("div",{class:`${n}-thing-header__extra`},e["header-extra"]?e["header-extra"]():t.titleExtra):null):null,e.description||t.description?a("div",{class:[`${n}-thing-main__description`,t.descriptionClass],style:t.descriptionStyle},e.description?e.description():t.description):null),e.default||t.content?a("div",{class:[`${n}-thing-main__content`,t.contentClass],style:t.contentStyle},e.default?e.default():t.content):null,e.footer?a("div",{class:`${n}-thing-main__footer`},e.footer()):null,e.action?a("div",{class:`${n}-thing-main__action`},e.action()):null))}}}),te=F("depot",()=>{async function t(){return(await N.get("/depot/readdepot")).data}return{getDepotinfo:t}}),ne={class:"card-container"},ae=J("br",null,null,-1),he={__name:"depot",setup(t){const e=te(),{getDepotinfo:g}=e,d=T([]);let s=T([]);async function $(){d.value=await g(),v()}function v(){s.value={...d.value[0]};for(const i in s.value)if(s.value.hasOwnProperty(i)){const u=s.value[i],n=Object.entries(u).map(([r,c])=>({key:r,...c})).sort((r,c)=>r.sort-c.sort);s.value[i]=n}}W($);const p=async()=>{try{await navigator.clipboard.writeText(d.value[1]),console.log("Text copied:",d.value[1])}catch(i){console.error("Failed to copy text:",i)}};return(i,u)=>{const n=q,r=U,c=Q,w=P,D=X,j=ee,E=K;return m(),C("div",ne,[o(n,{onClick:p,tag:"a",href:"https://arkntools.app/#/material",target:"_blank"},{default:l(()=>[_(" 明日方舟工具箱代码 点击复制 ")]),_:1}),o(r),o(E,{cols:"1",responsive:"screen"},{default:l(()=>[o(c,null,{default:l(()=>[_(" 扫描时间："+y(d.value[2])+" ",1),ae,_(" 注：万以下的数字并不会计入，如“龙门币 245万” “资质凭证 2万”"),o(r)]),_:1}),(m(!0),C(S,null,z(G(s),(O,k)=>(m(),R(c,{key:k},{default:l(()=>[o(w,null,{default:l(()=>[_(y(k.slice(1)),1)]),_:2},1024),o(E,{"x-gap":"10px","y-gap":"10px",cols:"2 m:6 l:6 ",responsive:"screen"},{default:l(()=>[(m(!0),C(S,null,z(O,x=>(m(),R(c,{key:x},{default:l(()=>[o(j,null,{avatar:l(()=>[o(D,{color:"000",size:"large",src:"/depot/"+x.icon+".webp"},null,8,["src"])]),header:l(()=>[_(y(x.key),1)]),description:l(()=>[_("拥有："+y(x.number),1)]),_:2},1024)]),_:2},1024))),128))]),_:2},1024),o(r)]),_:2},1024))),128))]),_:1})])}}};export{he as default};
