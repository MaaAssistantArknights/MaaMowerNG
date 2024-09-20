import{as as w,ar as h,av as c,B as z,ax as $,ay as l,j as f,aY as i,aA as T,H as B}from"./_plugin-vue_export-helper.js";import{an as H}from"./main.js";const R=w("h",`
 font-size: var(--n-font-size);
 font-weight: var(--n-font-weight);
 margin: var(--n-margin);
 transition: color .3s var(--n-bezier);
 color: var(--n-text-color);
`,[h("&:first-child",{marginTop:0}),c("prefix-bar",{position:"relative",paddingLeft:"var(--n-prefix-width)"},[c("align-text",{paddingLeft:0},[h("&::before",{left:"calc(-1 * var(--n-prefix-width))"})]),h("&::before",`
 content: "";
 width: var(--n-bar-width);
 border-radius: calc(var(--n-bar-width) / 2);
 transition: background-color .3s var(--n-bezier);
 left: 0;
 top: 0;
 bottom: 0;
 position: absolute;
 `),h("&::before",{backgroundColor:"var(--n-bar-color)"})])]),P=Object.assign(Object.assign({},l.props),{type:{type:String,default:"default"},prefix:String,alignText:Boolean}),n=r=>z({name:`H${r}`,props:P,setup(e){const{mergedClsPrefixRef:o,inlineThemeDisabled:s}=$(e),a=l("Typography","-h",R,H,e,o),d=f(()=>{const{type:g}=e,{common:{cubicBezierEaseInOut:m},self:{headerFontWeight:p,headerTextColor:b,[i("headerPrefixWidth",r)]:u,[i("headerFontSize",r)]:x,[i("headerMargin",r)]:v,[i("headerBarWidth",r)]:C,[i("headerBarColor",g)]:y}}=a.value;return{"--n-bezier":m,"--n-font-size":x,"--n-margin":v,"--n-bar-color":y,"--n-bar-width":C,"--n-font-weight":p,"--n-text-color":b,"--n-prefix-width":u}}),t=s?T(`h${r}`,f(()=>e.type[0]),d,e):void 0;return{mergedClsPrefix:o,cssVars:s?void 0:d,themeClass:t==null?void 0:t.themeClass,onRender:t==null?void 0:t.onRender}},render(){var e;const{prefix:o,alignText:s,mergedClsPrefix:a,cssVars:d,$slots:t}=this;return(e=this.onRender)===null||e===void 0||e.call(this),B(`h${r}`,{class:[`${a}-h`,`${a}-h${r}`,this.themeClass,{[`${a}-h--prefix-bar`]:o,[`${a}-h--align-text`]:s}],style:d},t)}}),j=n("1"),L=n("2");n("3");n("4");n("5");n("6");export{L as N,j as a};
