import{as as c,B as d,ax as m,ay as r,j as u,aA as h,H as f}from"./_plugin-vue_export-helper.js";import{an as p}from"./main.js";const v=c("a",`
 cursor: pointer;
 transition:
 color .3s var(--n-bezier),
 text-decoration-color .3s var(--n-bezier);
 text-decoration-color: var(--n-text-color);
 color: var(--n-text-color);
`),x=Object.assign({},r.props),y=d({name:"A",props:x,setup(e){const{mergedClsPrefixRef:o,inlineThemeDisabled:n}=m(e),a=r("Typography","-a",v,p,e,o),t=u(()=>{const{common:{cubicBezierEaseInOut:i},self:{aTextColor:l}}=a.value;return{"--n-text-color":l,"--n-bezier":i}}),s=n?h("a",void 0,t,e):void 0;return{mergedClsPrefix:o,cssVars:n?void 0:t,themeClass:s==null?void 0:s.themeClass,onRender:s==null?void 0:s.onRender}},render(){var e;return(e=this.onRender)===null||e===void 0||e.call(this),f("a",{class:[`${this.mergedClsPrefix}-a`,this.themeClass],style:this.cssVars},this.$slots)}});export{y as _};
