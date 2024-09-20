import{_ as De}from"./HelpText.js";import{c as We,u as Ue,_ as qe,a as Ke,b as Ae}from"./DropDown.js";import{ap as Ye,an as ze,aq as Xe,aM as Ge,B as re,H as r,bi as Ve,z as Qe,r as P,j as O,s as He,w as Le,b as ie,d as xe,as as te,ar as le,au as l,ax as Me,ay as se,D as ye,aA as je,b8 as Je,aB as Ze,n as ke,l as Re,bg as Se,av as I,at as $e,bH as et,aI as tt,aE as ve,aG as U,aY as q,bA as me,bj as E,bh as ot,aL as _e,bm as Ce,br as nt,bI as lt,bc as at,bs as v,bC as M,bv as B,bu as R,bo as c,bx as u,bt as X,bw as K,b3 as it,E as rt,aC as st,F as G,bD as Be,k as we,bF as ct,bG as dt,aX as ut,bE as Q}from"./_plugin-vue_export-helper.js";import{c as ht,f as ft,t as gt,u as bt,s as Te,a as pt}from"./main.js";import{a as vt,_ as mt}from"./Play.js";import{_ as _t}from"./op_select.js";import{u as wt}from"./Input.js";import"./Select.js";import"./Tag.js";import"./VirtualList.js";import"./Forward.js";import"./index.js";import"./get-slot.js";import"./Avatar.js";const xt=e=>{const{textColor2:o,modalColor:n,borderColor:i,fontSize:s,primaryColor:w}=e;return{loaderFontSize:s,loaderTextColor:o,loaderColor:n,loaderBorder:`1px solid ${i}`,loadingColor:w}},yt=Ye({name:"Log",common:ze,peers:{Scrollbar:Xe,Code:We},self:xt}),kt=yt,Ct=e=>{const{primaryColor:o,opacityDisabled:n,borderRadius:i,textColor3:s}=e;return Object.assign(Object.assign({},ht),{iconColor:s,textColor:"white",loadingColor:o,opacityDisabled:n,railColor:"rgba(0, 0, 0, .14)",railColorActive:o,buttonBoxShadow:"0 1px 4px 0 rgba(0, 0, 0, 0.3), inset 0 0 1px 0 rgba(0, 0, 0, 0.05)",buttonColor:"#FFF",railBorderRadiusSmall:i,railBorderRadiusMedium:i,railBorderRadiusLarge:i,buttonBorderRadiusSmall:i,buttonBorderRadiusMedium:i,buttonBorderRadiusLarge:i,boxShadowFocus:`0 0 0 2px ${Ge(o,{alpha:.2})}`})},Rt={name:"Switch",common:ze,self:Ct},St=Rt,$t=re({name:"LogLoader",props:{clsPrefix:{type:String,required:!0}},setup(){return{locale:wt("Log").localeRef}},render(){const{clsPrefix:e}=this;return r("div",{class:`${e}-log-loader`},r(Ve,{clsPrefix:e,strokeWidth:24,scale:.85}),r("span",{class:`${e}-log-loader__content`},this.locale.loading))}}),Fe=Qe("n-log"),Bt=re({props:{line:{type:String,default:""}},setup(e){const{trimRef:o,highlightRef:n,languageRef:i,mergedHljsRef:s}=xe(Fe),w=P(null),x=O(()=>o.value?e.line.trim():e.line);function h(){w.value&&(w.value.innerHTML=L(i.value,x.value))}function L(m,k){const{value:d}=s;return d&&m&&d.getLanguage(m)?d.highlight(k,{language:m}).value:k}return He(()=>{n.value&&h()}),Le(ie(e,"line"),()=>{n.value&&h()}),{highlight:n,selfRef:w,maybeTrimmedLines:x}},render(){const{highlight:e,maybeTrimmedLines:o}=this;return r("pre",{ref:"selfRef"},e?null:o)}}),Tt=te("log",`
 position: relative;
 box-sizing: border-box;
 transition: border-color .3s var(--n-bezier);
`,[le("pre",`
 white-space: pre-wrap;
 word-break: break-word;
 margin: 0;
 `),te("log-loader",`
 transition:
 color .3s var(--n-bezier),
 background-color .3s var(--n-bezier),
 border-color .3s var(--n-bezier);
 box-sizing: border-box;
 position: absolute;
 right: 16px;
 top: 8px;
 height: 34px;
 border-radius: 17px;
 line-height: 34px;
 white-space: nowrap;
 overflow: hidden;
 border: var(--n-loader-border);
 color: var(--n-loader-text-color);
 background-color: var(--n-loader-color);
 font-size: var(--n-loader-font-size);
 `,[ft(),l("content",`
 display: inline-block;
 vertical-align: bottom;
 line-height: 34px;
 padding-left: 40px;
 padding-right: 20px;
 white-space: nowrap;
 `),te("base-loading",`
 color: var(--n-loading-color);
 position: absolute;
 left: 12px;
 top: calc(50% - 10px);
 font-size: 20px;
 width: 20px;
 height: 20px;
 display: inline-block;
 `)])]),zt=Object.assign(Object.assign({},se.props),{loading:Boolean,trim:Boolean,log:String,fontSize:{type:Number,default:14},lines:{type:Array,default:()=>[]},lineHeight:{type:Number,default:1.25},language:String,rows:{type:Number,default:15},offsetTop:{type:Number,default:0},offsetBottom:{type:Number,default:0},hljs:Object,onReachTop:Function,onReachBottom:Function,onRequireMore:Function}),Vt=re({name:"Log",props:zt,setup(e){const{mergedClsPrefixRef:o,inlineThemeDisabled:n}=Me(e),i=P(!1),s=O(()=>e.language!==void 0),w=O(()=>`calc(${Math.round(e.rows*e.lineHeight*e.fontSize)}px)`),x=O(()=>{const{log:g}=e;return g?g.split(`
`):e.lines}),h=P(null),L=se("Log","-log",Tt,kt,e,o);function m(g){const p=g.target,V=p.firstElementChild;if(i.value){ke(()=>{i.value=!1});return}const H=p.offsetHeight,_=p.scrollTop,C=V.offsetHeight,t=_,y=C-_-H;if(t<=e.offsetTop){const{onReachTop:f,onRequireMore:b}=e;b&&b("top"),f&&f()}if(y<=e.offsetBottom){const{onReachBottom:f,onRequireMore:b}=e;b&&b("bottom"),f&&f()}}const k=gt(d,300);function d(g){if(i.value){ke(()=>{i.value=!1});return}if(h.value){const{containerRef:p,contentRef:V}=h.value;if(p&&V){const H=p.offsetHeight,_=p.scrollTop,C=V.offsetHeight,t=_,y=C-_-H,f=g.deltaY;if(t===0&&f<0){const{onRequireMore:b}=e;b&&b("top")}if(y<=0&&f>0){const{onRequireMore:b}=e;b&&b("bottom")}}}}function a(g){const{value:p}=h;if(!p)return;const{silent:V,top:H,position:_}=g;V&&(i.value=!0),H!==void 0?p.scrollTo({left:0,top:H}):(_==="bottom"||_==="top")&&p.scrollTo({position:_})}function T(g=!1){Re("log","`scrollToTop` is deprecated, please use `scrollTo({ position: 'top'})` instead."),a({position:"top",silent:g})}function z(g=!1){Re("log","`scrollToTop` is deprecated, please use `scrollTo({ position: 'bottom'})` instead."),a({position:"bottom",silent:g})}ye(Fe,{languageRef:ie(e,"language"),mergedHljsRef:Ue(e),trimRef:ie(e,"trim"),highlightRef:s});const J={scrollTo:a},A=O(()=>{const{self:{loaderFontSize:g,loaderTextColor:p,loaderColor:V,loaderBorder:H,loadingColor:_},common:{cubicBezierEaseInOut:C}}=L.value;return{"--n-bezier":C,"--n-loader-font-size":g,"--n-loader-border":H,"--n-loader-color":V,"--n-loader-text-color":p,"--n-loading-color":_}}),S=n?je("log",void 0,A,e):void 0;return Object.assign(Object.assign({},J),{mergedClsPrefix:o,scrollbarRef:h,mergedTheme:L,styleHeight:w,mergedLines:x,scrollToTop:T,scrollToBottom:z,handleWheel:k,handleScroll:m,cssVars:n?void 0:A,themeClass:S==null?void 0:S.themeClass,onRender:S==null?void 0:S.onRender})},render(){const{mergedClsPrefix:e,mergedTheme:o,onRender:n}=this;return n==null||n(),r("div",{class:[`${e}-log`,this.themeClass],style:[{lineHeight:this.lineHeight,height:this.styleHeight},this.cssVars],onWheelPassive:this.handleWheel},[r(Je,{ref:"scrollbarRef",theme:o.peers.Scrollbar,themeOverrides:o.peerOverrides.Scrollbar,onScroll:this.handleScroll},{default:()=>r(qe,{internalNoHighlight:!0,internalFontSize:this.fontSize,theme:o.peers.Code,themeOverrides:o.peerOverrides.Code},{default:()=>this.mergedLines.map((i,s)=>r(Bt,{key:s,line:i}))})}),r(Ze,{name:"fade-in-scale-up-transition"},{default:()=>this.loading?r($t,{clsPrefix:e}):null})])}}),Ht=te("switch",`
 height: var(--n-height);
 min-width: var(--n-width);
 vertical-align: middle;
 user-select: none;
 -webkit-user-select: none;
 display: inline-flex;
 outline: none;
 justify-content: center;
 align-items: center;
`,[l("children-placeholder",`
 height: var(--n-rail-height);
 display: flex;
 flex-direction: column;
 overflow: hidden;
 pointer-events: none;
 visibility: hidden;
 `),l("rail-placeholder",`
 display: flex;
 flex-wrap: none;
 `),l("button-placeholder",`
 width: calc(1.75 * var(--n-rail-height));
 height: var(--n-rail-height);
 `),te("base-loading",`
 position: absolute;
 top: 50%;
 left: 50%;
 transform: translateX(-50%) translateY(-50%);
 font-size: calc(var(--n-button-width) - 4px);
 color: var(--n-loading-color);
 transition: color .3s var(--n-bezier);
 `,[Se({left:"50%",top:"50%",originalTransform:"translateX(-50%) translateY(-50%)"})]),l("checked, unchecked",`
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
 box-sizing: border-box;
 position: absolute;
 white-space: nowrap;
 top: 0;
 bottom: 0;
 display: flex;
 align-items: center;
 line-height: 1;
 `),l("checked",`
 right: 0;
 padding-right: calc(1.25 * var(--n-rail-height) - var(--n-offset));
 `),l("unchecked",`
 left: 0;
 justify-content: flex-end;
 padding-left: calc(1.25 * var(--n-rail-height) - var(--n-offset));
 `),le("&:focus",[l("rail",`
 box-shadow: var(--n-box-shadow-focus);
 `)]),I("round",[l("rail","border-radius: calc(var(--n-rail-height) / 2);",[l("button","border-radius: calc(var(--n-button-height) / 2);")])]),$e("disabled",[$e("icon",[I("rubber-band",[I("pressed",[l("rail",[l("button","max-width: var(--n-button-width-pressed);")])]),l("rail",[le("&:active",[l("button","max-width: var(--n-button-width-pressed);")])]),I("active",[I("pressed",[l("rail",[l("button","left: calc(100% - var(--n-offset) - var(--n-button-width-pressed));")])]),l("rail",[le("&:active",[l("button","left: calc(100% - var(--n-offset) - var(--n-button-width-pressed));")])])])])])]),I("active",[l("rail",[l("button","left: calc(100% - var(--n-button-width) - var(--n-offset))")])]),l("rail",`
 overflow: hidden;
 height: var(--n-rail-height);
 min-width: var(--n-rail-width);
 border-radius: var(--n-rail-border-radius);
 cursor: pointer;
 position: relative;
 transition:
 opacity .3s var(--n-bezier),
 background .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 background-color: var(--n-rail-color);
 `,[l("button-icon",`
 color: var(--n-icon-color);
 transition: color .3s var(--n-bezier);
 font-size: calc(var(--n-button-height) - 4px);
 position: absolute;
 left: 0;
 right: 0;
 top: 0;
 bottom: 0;
 display: flex;
 justify-content: center;
 align-items: center;
 line-height: 1;
 `,[Se()]),l("button",`
 align-items: center; 
 top: var(--n-offset);
 left: var(--n-offset);
 height: var(--n-button-height);
 width: var(--n-button-width-pressed);
 max-width: var(--n-button-width);
 border-radius: var(--n-button-border-radius);
 background-color: var(--n-button-color);
 box-shadow: var(--n-button-box-shadow);
 box-sizing: border-box;
 cursor: inherit;
 content: "";
 position: absolute;
 transition:
 background-color .3s var(--n-bezier),
 left .3s var(--n-bezier),
 opacity .3s var(--n-bezier),
 max-width .3s var(--n-bezier),
 box-shadow .3s var(--n-bezier);
 `)]),I("active",[l("rail","background-color: var(--n-rail-color-active);")]),I("loading",[l("rail",`
 cursor: wait;
 `)]),I("disabled",[l("rail",`
 cursor: not-allowed;
 opacity: .5;
 `)])]),Lt=Object.assign(Object.assign({},se.props),{size:{type:String,default:"medium"},value:{type:[String,Number,Boolean],default:void 0},loading:Boolean,defaultValue:{type:[String,Number,Boolean],default:!1},disabled:{type:Boolean,default:void 0},round:{type:Boolean,default:!0},"onUpdate:value":[Function,Array],onUpdateValue:[Function,Array],checkedValue:{type:[String,Number,Boolean],default:!0},uncheckedValue:{type:[String,Number,Boolean],default:!1},railStyle:Function,rubberBand:{type:Boolean,default:!0},onChange:[Function,Array]});let ee;const Mt=re({name:"Switch",props:Lt,setup(e){ee===void 0&&(typeof CSS<"u"?typeof CSS.supports<"u"?ee=CSS.supports("width","max(1px)"):ee=!1:ee=!0);const{mergedClsPrefixRef:o,inlineThemeDisabled:n}=Me(e),i=se("Switch","-switch",Ht,St,e,o),s=et(e),{mergedSizeRef:w,mergedDisabledRef:x}=s,h=P(e.defaultValue),L=ie(e,"value"),m=tt(L,h),k=O(()=>m.value===e.checkedValue),d=P(!1),a=P(!1),T=O(()=>{const{railStyle:t}=e;if(t)return t({focused:a.value,checked:k.value})});function z(t){const{"onUpdate:value":y,onChange:f,onUpdateValue:b}=e,{nTriggerFormInput:Z,nTriggerFormChange:D}=s;y&&_e(y,t),b&&_e(b,t),f&&_e(f,t),h.value=t,Z(),D()}function J(){const{nTriggerFormFocus:t}=s;t()}function A(){const{nTriggerFormBlur:t}=s;t()}function S(){e.loading||x.value||(m.value!==e.checkedValue?z(e.checkedValue):z(e.uncheckedValue))}function g(){a.value=!0,J()}function p(){a.value=!1,A(),d.value=!1}function V(t){e.loading||x.value||t.key===" "&&(m.value!==e.checkedValue?z(e.checkedValue):z(e.uncheckedValue),d.value=!1)}function H(t){e.loading||x.value||t.key===" "&&(t.preventDefault(),d.value=!0)}const _=O(()=>{const{value:t}=w,{self:{opacityDisabled:y,railColor:f,railColorActive:b,buttonBoxShadow:Z,buttonColor:D,boxShadowFocus:Y,loadingColor:ce,textColor:de,iconColor:ue,[q("buttonHeight",t)]:F,[q("buttonWidth",t)]:$,[q("buttonWidthPressed",t)]:he,[q("railHeight",t)]:N,[q("railWidth",t)]:W,[q("railBorderRadius",t)]:fe,[q("buttonBorderRadius",t)]:Ie},common:{cubicBezierEaseInOut:Ee}}=i.value;let ge,be,pe;return ee?(ge=`calc((${N} - ${F}) / 2)`,be=`max(${N}, ${F})`,pe=`max(${W}, calc(${W} + ${F} - ${N}))`):(ge=me((E(N)-E(F))/2),be=me(Math.max(E(N),E(F))),pe=E(N)>E(F)?W:me(E(W)+E(F)-E(N))),{"--n-bezier":Ee,"--n-button-border-radius":Ie,"--n-button-box-shadow":Z,"--n-button-color":D,"--n-button-width":$,"--n-button-width-pressed":he,"--n-button-height":F,"--n-height":be,"--n-offset":ge,"--n-opacity-disabled":y,"--n-rail-border-radius":fe,"--n-rail-color":f,"--n-rail-color-active":b,"--n-rail-height":N,"--n-rail-width":W,"--n-width":pe,"--n-box-shadow-focus":Y,"--n-loading-color":ce,"--n-text-color":de,"--n-icon-color":ue}}),C=n?je("switch",O(()=>w.value[0]),_,e):void 0;return{handleClick:S,handleBlur:p,handleFocus:g,handleKeyup:V,handleKeydown:H,mergedRailStyle:T,pressed:d,mergedClsPrefix:o,mergedValue:m,checked:k,mergedDisabled:x,cssVars:n?void 0:_,themeClass:C==null?void 0:C.themeClass,onRender:C==null?void 0:C.onRender}},render(){const{mergedClsPrefix:e,mergedDisabled:o,checked:n,mergedRailStyle:i,onRender:s,$slots:w}=this;s==null||s();const{checked:x,unchecked:h,icon:L,"checked-icon":m,"unchecked-icon":k}=w,d=!(ve(L)&&ve(m)&&ve(k));return r("div",{role:"switch","aria-checked":n,class:[`${e}-switch`,this.themeClass,d&&`${e}-switch--icon`,n&&`${e}-switch--active`,o&&`${e}-switch--disabled`,this.round&&`${e}-switch--round`,this.loading&&`${e}-switch--loading`,this.pressed&&`${e}-switch--pressed`,this.rubberBand&&`${e}-switch--rubber-band`],tabindex:this.mergedDisabled?void 0:0,style:this.cssVars,onClick:this.handleClick,onFocus:this.handleFocus,onBlur:this.handleBlur,onKeyup:this.handleKeyup,onKeydown:this.handleKeydown},r("div",{class:`${e}-switch__rail`,"aria-hidden":"true",style:i},U(x,a=>U(h,T=>a||T?r("div",{"aria-hidden":!0,class:`${e}-switch__children-placeholder`},r("div",{class:`${e}-switch__rail-placeholder`},r("div",{class:`${e}-switch__button-placeholder`}),a),r("div",{class:`${e}-switch__rail-placeholder`},r("div",{class:`${e}-switch__button-placeholder`}),T)):null)),r("div",{class:`${e}-switch__button`},U(L,a=>U(m,T=>U(k,z=>r(ot,null,{default:()=>this.loading?r(Ve,{key:"loading",clsPrefix:e,strokeWidth:20}):this.checked&&(T||a)?r("div",{class:`${e}-switch__button-icon`,key:T?"checked-icon":"icon"},T||a):!this.checked&&(z||a)?r("div",{class:`${e}-switch__button-icon`,key:z?"unchecked-icon":"icon"},z||a):null})))),U(x,a=>a&&r("div",{key:"checked",class:`${e}-switch__checked`},a)),U(h,a=>a&&r("div",{key:"unchecked",class:`${e}-switch__unchecked`},a)))))}});var Ne={};Object.defineProperty(Ne,"__esModule",{value:!0});const ae=Ce,jt={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 512 512"},Ft=(0,ae.createElementVNode)("path",{d:"M392 432H120a40 40 0 0 1-40-40V120a40 40 0 0 1 40-40h272a40 40 0 0 1 40 40v272a40 40 0 0 1-40 40z",fill:"currentColor"},null,-1),Nt=[Ft];var Pt=Ne.default=(0,ae.defineComponent)({name:"Stop",render:function(o,n){return(0,ae.openBlock)(),(0,ae.createElementBlock)("svg",jt,Nt)}}),Pe={};Object.defineProperty(Pe,"__esModule",{value:!0});const oe=Ce,Ot={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 20 20"},It=(0,oe.createElementVNode)("g",{fill:"none"},[(0,oe.createElementVNode)("path",{d:"M10.5 8.826l.874.998a.5.5 0 0 0 .752-.658l-1.75-2a.5.5 0 0 0-.752 0l-1.75 2a.5.5 0 0 0 .752.658l.874-.998v3.679a.5.5 0 0 0 1 0v-3.68zM4 16a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4zm-1-2a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9h-3.834a1.495 1.495 0 0 0-.287-.493L12.435 8H17V6a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v2h4.565l-.444.507c-.13.15-.226.317-.287.493H3v5z",fill:"currentColor"})],-1),Et=[It];var Dt=Pe.default=(0,oe.defineComponent)({name:"PanelTopContract20Regular",render:function(o,n){return(0,oe.openBlock)(),(0,oe.createElementBlock)("svg",Ot,Et)}}),Oe={};Object.defineProperty(Oe,"__esModule",{value:!0});const ne=Ce,Wt={xmlns:"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink",viewBox:"0 0 20 20"},Ut=(0,ne.createElementVNode)("g",{fill:"none"},[(0,ne.createElementVNode)("path",{d:"M10.5 11.174l.874-.998a.5.5 0 0 1 .752.658l-1.75 2a.5.5 0 0 1-.752 0l-1.75-2a.5.5 0 1 1 .752-.658l.874.998V7.495a.5.5 0 0 1 1 0v3.68zM4 16a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4zm-1-2a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V9h-5.5V8H17V6a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v2h5.5v1H3v5z",fill:"currentColor"})],-1),qt=[Ut];var Kt=Oe.default=(0,ne.defineComponent)({name:"PanelTopExpand20Regular",render:function(o,n){return(0,ne.openBlock)(),(0,ne.createElementBlock)("svg",Wt,qt)}});const j=e=>(ct("data-v-97f6834c"),e=e(),dt(),e),At={class:"home-container"},Yt=j(()=>u("div",{class:"log-bg"},null,-1)),Xt=j(()=>u("thead",null,[u("tr",null,[u("th",null,"时间"),u("th",{colspan:2},"任务")])],-1)),Gt=["rowspan"],Qt={key:1},Jt={colspan:2},Zt={class:"action-container"},eo=j(()=>u("div",null,"目前只糊了一个勉强能用的版本，其他功能敬请期待",-1)),to=j(()=>u("div",null,"只开放了空任务/专精任务",-1)),oo=j(()=>u("div",null,"只能增，不能删！！谨慎填写任务",-1)),no=j(()=>u("div",null,"如果 mower 休息到 00:30，新增的 00:15 的任务是不会被执行的，因为此时在休息",-1)),lo=j(()=>u("div",null,"所以最好在 00:00 mower运行的时候添加 00:15 的任务了，考验手速的时候到了",-1)),ao=j(()=>u("div",null,"空任务，请确保任务房间名字，干员数量正确（没有判定）",-1)),io=j(()=>u("div",null,"专精任务，UI有详细说明；新增完毕，UI上面的表会实时反馈",-1)),ro=j(()=>u("div",null,"在Q群或者频道提以上问题，看心情踢人",-1)),so=j(()=>u("div",{class:"expand"},null,-1)),co={class:"scroll-container"},uo={key:0,class:"scroll-label"},ho={__name:"Log",setup(e){lt(y=>({"23b16ac2":c(_)}));const o=bt(),{log:n,log_mobile:i,running:s,log_lines:w,task_list:x,waiting:h,get_task_id:L}=Te(o),{get_tasks:m}=o,k=xe("axios"),d=xe("mobile"),a=P(!0);function T(){ke(()=>{var y;(y=document.querySelector("pre:last-child"))==null||y.scrollIntoView()})}function z(){a.value&&T()}Le(()=>[n,x],()=>{z()},{deep:!0}),He(()=>{m()}),at(()=>{clearTimeout(L.value)});function J(){s.value=!0,w.value=[],k.get("/start"),m()}function A(){h.value=!0,k.get("/stop").then(y=>{s.value=!y.data,h.value=!1})}const S=P(!0),g=P(!1),p=P(!0);ye("show_task",g),ye("add_task",p);const V=pt(),{theme:H}=Te(V),_=O(()=>H.value=="light"?.2:.3);function C(){k.get("/stop-maa")}const t=[{label:"停止Maa",key:"maa"}];return(y,f)=>{const b=_t,Z=Vt,D=ut,Y=it,ce=Ke,de=Ae,ue=De,F=Mt;return v(),M("div",At,[Yt,B(b,{class:"task-table",size:"small","single-line":!1},{default:R(()=>[Xt,rt(u("tbody",null,[(v(!0),M(G,null,Be(c(x),$=>(v(),M(G,null,[Object.keys($.plan).length?(v(!0),M(G,{key:0},Be($.plan,(he,N,W)=>(v(),M("tr",null,[W==0?(v(),M("td",{key:0,rowspan:Object.keys($.plan).length},Q($.time.split("T")[1].split(".")[0]),9,Gt)):K("",!0),u("td",null,Q(N),1),u("td",null,Q(he.map(fe=>fe||"_").join(", ")),1)]))),256)):(v(),M("tr",Qt,[u("td",null,Q($.time.split("T")[1].split(".")[0]),1),u("td",Jt,Q($.meta_data)+Q($.type.display_value),1)]))],64))),256))],512),[[st,!c(d)||S.value]])]),_:1}),B(Z,{class:"log",log:c(d)?c(i):c(n),language:"mower",style:{"user-select":"text"}},null,8,["log"]),u("div",Zt,[c(s)?(v(),X(ce,{key:0,select:C,options:t,type:"error",up:!0},{default:R(()=>[B(Y,{type:"error",onClick:A,loading:c(h),disabled:c(h)},{icon:R(()=>[B(D,null,{default:R(()=>[B(c(Pt))]),_:1})]),default:R(()=>[c(d)?K("",!0):(v(),M(G,{key:0},[we("立即停止")],64))]),_:1},8,["loading","disabled"])]),_:1})):(v(),X(Y,{key:1,type:"primary",onClick:J,loading:c(h),disabled:c(h)},{icon:R(()=>[B(D,null,{default:R(()=>[B(c(vt))]),_:1})]),default:R(()=>[c(d)?K("",!0):(v(),M(G,{key:0},[we("开始执行")],64))]),_:1},8,["loading","disabled"])),B(de),B(Y,{type:"warning",onClick:f[0]||(f[0]=$=>g.value=!0)},{icon:R(()=>[B(D,null,{default:R(()=>[B(c(mt))]),_:1})]),default:R(()=>[c(d)?K("",!0):(v(),M(G,{key:0},[we("新增任务")],64))]),_:1}),c(d)?K("",!0):(v(),X(ue,{key:2},{default:R(()=>[eo,to,oo,no,lo,ao,io,ro]),_:1})),so,u("div",co,[B(F,{value:a.value,"onUpdate:value":f[1]||(f[1]=$=>a.value=$)},null,8,["value"]),c(d)?K("",!0):(v(),M("span",uo,"自动滚动"))])]),c(d)?(v(),X(Y,{key:0,class:"toggle-table-collapse-btn",size:"small",onClick:f[2]||(f[2]=$=>S.value=!S.value),focusable:!1},{icon:R(()=>[B(D,null,{default:R(()=>[S.value?(v(),X(c(Dt),{key:0})):(v(),X(c(Kt),{key:1}))]),_:1})]),_:1})):K("",!0)])}}},$o=nt(ho,[["__scopeId","data-v-97f6834c"]]);export{$o as default};
