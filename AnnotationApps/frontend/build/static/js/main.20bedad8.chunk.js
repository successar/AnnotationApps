(this.webpackJsonpstreamlit_component_template=this.webpackJsonpstreamlit_component_template||[]).push([[0],{13:function(e,t,n){"use strict";n.r(t);var a=n(4),o=n(2),i=n.n(o),r=n(1);function s(){var e=i()("div[data-type=common]").data(),t=i()(this).data(),n=Object(r.a)(Object(r.a)({},e),t);delete n.type;var a=n.tablename;return delete n.tablename,{api:"add_or_delete_multiple",tablename:a,common_keys:n,multi_keys:i()(this).find(".highlightable").map((function(){return[[i()(this).data(),this.classList.contains("rationale")]]})).get()}}function l(){var e=window.getSelection();if(e){var t=function(e){var t=e.startContainer,n=e.endContainer;if(t==n)return[t];var a=[];for(;t&&t!=n;)a.push(t=c(t));t=e.startContainer;for(;t&&t!=e.commonAncestorContainer;)a.unshift(t),t=t.parentNode;return a}(e.getRangeAt(0)),n=[];t.forEach((function(e){if(e.nodeType===Node.TEXT_NODE&&(e=e.parentNode),e.nodeType===Node.ELEMENT_NODE&&e.classList.contains("highlightable")){if(n.includes(e))return[];n.push(e),i()(e).toggleClass("rationale")}})),e.removeAllRanges()}}function c(e){if(e.hasChildNodes())return e.firstChild;for(;e&&!e.nextSibling;)e=e.parentNode;return e?e.nextSibling:null}function d(){var e=i()("div[data-type=common]").data(),t=i()(this).data(),n=Object(r.a)(Object(r.a)({},e),t);delete n.type;var a=n.tablename;return delete n.tablename,{api:"add_or_delete",tablename:a,keys:n,value:i()(this).prop("checked")}}function u(){var e=[];return e=(e=e.concat(i()("input[type=checkbox].db").map(d).get())).concat(i()(".highlight").map(s).get()),console.log(e),e}a.a.events.addEventListener(a.a.RENDER_EVENT,(function(e){var t=e.detail;i()("#docdiv").html(t.args.data),console.log("Updating"),i()(".highlight").on("mouseup",l),i()("#savenext").on("click",(function(){var e=u();a.a.setComponentValue({done:!0,next:!0,values:e})})),i()("#save").on("click",(function(){var e=u();a.a.setComponentValue({done:!0,next:!1,values:e})})),a.a.setFrameHeight()})),a.a.setComponentReady(),a.a.setFrameHeight()},7:function(e,t,n){e.exports=n(13)}},[[7,1,2]]]);
//# sourceMappingURL=main.20bedad8.chunk.js.map