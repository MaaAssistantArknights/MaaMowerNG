import{B as J,s as Z,c1 as Q,bZ as ee,j as T,r as R,A as te,bj as Y,H as I,aF as ie,bf as $,J as le,bA as B}from"./_plugin-vue_export-helper.js";import{ap as ne,aq as O,O as se}from"./main.js";function D(l){return l&-l}class oe{constructor(i,s){this.l=i,this.min=s;const u=new Array(i+1);for(let o=0;o<i+1;++o)u[o]=0;this.ft=u}add(i,s){if(s===0)return;const{l:u,ft:o}=this;for(i+=1;i<=u;)o[i]+=s,i+=D(i)}get(i){return this.sum(i+1)-this.sum(i)}sum(i){if(i===void 0&&(i=this.l),i<=0)return 0;const{ft:s,min:u,l:o}=this;if(i>o)throw new Error("[FinweckTree.sum]: `i` is larger than length.");let r=i*u;for(;i>0;)r+=s[i],i-=D(i);return r}getBound(i){let s=0,u=this.l;for(;u>s;){const o=Math.floor((s+u)/2),r=this.sum(o);if(r>i){u=o;continue}else if(r<i){if(s===o)return this.sum(s+1)<=i?s+1:o;s=o}else return o}return s}}let H;function re(){return typeof document>"u"?!1:(H===void 0&&("matchMedia"in window?H=window.matchMedia("(pointer:coarse)").matches:H=!1),H)}let W;function X(){return typeof document>"u"?1:(W===void 0&&(W="chrome"in window?window.devicePixelRatio:1),W)}const ae=O(".v-vl",{maxHeight:"inherit",height:"100%",overflow:"auto",minWidth:"1px"},[O("&:not(.v-vl--show-scrollbar)",{scrollbarWidth:"none"},[O("&::-webkit-scrollbar, &::-webkit-scrollbar-track-piece, &::-webkit-scrollbar-thumb",{width:0,height:0,display:"none"})])]),fe=J({name:"VirtualList",inheritAttrs:!1,props:{showScrollbar:{type:Boolean,default:!0},items:{type:Array,default:()=>[]},itemSize:{type:Number,required:!0},itemResizable:Boolean,itemsStyle:[String,Object],visibleItemsTag:{type:[String,Object],default:"div"},visibleItemsProps:Object,ignoreItemResize:Boolean,onScroll:Function,onWheel:Function,onResize:Function,defaultScrollKey:[Number,String],defaultScrollIndex:Number,keyField:{type:String,default:"key"},paddingTop:{type:[Number,String],default:0},paddingBottom:{type:[Number,String],default:0}},setup(l){const i=le();ae.mount({id:"vueuc/virtual-list",head:!0,anchorMetaName:ne,ssr:i}),Z(()=>{const{defaultScrollIndex:e,defaultScrollKey:t}=l;e!=null?z({index:e}):t!=null&&z({key:t})});let s=!1,u=!1;Q(()=>{if(s=!1,!u){u=!0;return}z({top:E.value,left:x})}),ee(()=>{s=!0,u||(u=!0)});const o=T(()=>{const e=new Map,{keyField:t}=l;return l.items.forEach((n,c)=>{e.set(n[t],c)}),e}),r=R(null),g=R(void 0),m=new Map,b=T(()=>{const{items:e,itemSize:t,keyField:n}=l,c=new oe(e.length,t);return e.forEach((f,d)=>{const a=f[n],h=m.get(a);h!==void 0&&c.add(d,h)}),c}),w=R(0);let x=0;const E=R(0),_=te(()=>Math.max(b.value.getBound(E.value-Y(l.paddingTop))-1,0)),q=T(()=>{const{value:e}=g;if(e===void 0)return[];const{items:t,itemSize:n}=l,c=_.value,f=Math.min(c+Math.ceil(e/n+1),t.length-1),d=[];for(let a=c;a<=f;++a)d.push(t[a]);return d}),z=(e,t)=>{if(typeof e=="number"){M(e,t,"auto");return}const{left:n,top:c,index:f,key:d,position:a,behavior:h,debounce:v=!0}=e;if(n!==void 0||c!==void 0)M(n,c,h);else if(f!==void 0)V(f,h,v);else if(d!==void 0){const L=o.value.get(d);L!==void 0&&V(L,h,v)}else a==="bottom"?M(0,Number.MAX_SAFE_INTEGER,h):a==="top"&&M(0,0,h)};let S,k=null;function V(e,t,n){const{value:c}=b,f=c.sum(e)+Y(l.paddingTop);if(!n)r.value.scrollTo({left:0,top:f,behavior:t});else{S=e,k!==null&&window.clearTimeout(k),k=window.setTimeout(()=>{S=void 0,k=null},16);const{scrollTop:d,offsetHeight:a}=r.value;if(f>d){const h=c.get(e);f+h<=d+a||r.value.scrollTo({left:0,top:f+h-a,behavior:t})}else r.value.scrollTo({left:0,top:f,behavior:t})}}function M(e,t,n){r.value.scrollTo({left:e,top:t,behavior:n})}function C(e,t){var n,c,f;if(s||l.ignoreItemResize||P(t.target))return;const{value:d}=b,a=o.value.get(e),h=d.get(a),v=(f=(c=(n=t.borderBoxSize)===null||n===void 0?void 0:n[0])===null||c===void 0?void 0:c.blockSize)!==null&&f!==void 0?f:t.contentRect.height;if(v===h)return;v-l.itemSize===0?m.delete(e):m.set(e,v-l.itemSize);const p=v-h;if(p===0)return;d.add(a,p);const y=r.value;if(y!=null){if(S===void 0){const N=d.sum(a);y.scrollTop>N&&y.scrollBy(0,p)}else if(a<S)y.scrollBy(0,p);else if(a===S){const N=d.sum(a);v+N>y.scrollTop+y.offsetHeight&&y.scrollBy(0,p)}A()}w.value++}const j=!re();let F=!1;function K(e){var t;(t=l.onScroll)===null||t===void 0||t.call(l,e),(!j||!F)&&A()}function U(e){var t;if((t=l.onWheel)===null||t===void 0||t.call(l,e),j){const n=r.value;if(n!=null){if(e.deltaX===0&&(n.scrollTop===0&&e.deltaY<=0||n.scrollTop+n.offsetHeight>=n.scrollHeight&&e.deltaY>=0))return;e.preventDefault(),n.scrollTop+=e.deltaY/X(),n.scrollLeft+=e.deltaX/X(),A(),F=!0,se(()=>{F=!1})}}}function G(e){if(s||P(e.target)||e.contentRect.height===g.value)return;g.value=e.contentRect.height;const{onResize:t}=l;t!==void 0&&t(e)}function A(){const{value:e}=r;e!=null&&(E.value=e.scrollTop,x=e.scrollLeft)}function P(e){let t=e;for(;t!==null;){if(t.style.display==="none")return!0;t=t.parentElement}return!1}return{listHeight:g,listStyle:{overflow:"auto"},keyToIndex:o,itemsStyle:T(()=>{const{itemResizable:e}=l,t=B(b.value.sum());return w.value,[l.itemsStyle,{boxSizing:"content-box",height:e?"":t,minHeight:e?t:"",paddingTop:B(l.paddingTop),paddingBottom:B(l.paddingBottom)}]}),visibleItemsStyle:T(()=>(w.value,{transform:`translateY(${B(b.value.sum(_.value))})`})),viewportItems:q,listElRef:r,itemsElRef:R(null),scrollTo:z,handleListResize:G,handleListScroll:K,handleListWheel:U,handleItemResize:C}},render(){const{itemResizable:l,keyField:i,keyToIndex:s,visibleItemsTag:u}=this;return I($,{onResize:this.handleListResize},{default:()=>{var o,r;return I("div",ie(this.$attrs,{class:["v-vl",this.showScrollbar&&"v-vl--show-scrollbar"],onScroll:this.handleListScroll,onWheel:this.handleListWheel,ref:"listElRef"}),[this.items.length!==0?I("div",{ref:"itemsElRef",class:"v-vl-items",style:this.itemsStyle},[I(u,Object.assign({class:"v-vl-visible-items",style:this.visibleItemsStyle},this.visibleItemsProps),{default:()=>this.viewportItems.map(g=>{const m=g[i],b=s.get(m),w=this.$slots.default({item:g,index:b})[0];return l?I($,{key:m,onResize:x=>this.handleItemResize(m,x)},{default:()=>w}):(w.key=m,w)})})]):(r=(o=this.$slots).empty)===null||r===void 0?void 0:r.call(o)])}})}});export{fe as V};