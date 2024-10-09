import bootstrap from "bootstrap/dist/js/bootstrap";



// 初始化工具提示（Tooltips）

export default function setTooltip() {

  // 获取所有带有 `data-bs-toggle="tooltip"` 属性的元素，并将其转换为数组

  var tooltipTriggerList = [].slice.call(

    document.querySelectorAll('[data-bs-toggle="tooltip"]')

  );

  

  // 遍历所有触发元素，并为每个元素创建一个新的 Bootstrap Tooltip 实例

  // eslint-disable-next-line no-unused-vars

  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

    return new bootstrap.Tooltip(tooltipTriggerEl);

  });

}