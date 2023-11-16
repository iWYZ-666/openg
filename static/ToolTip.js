const tooltip = new G6.Tooltip({
    offsetX: 10,
    offsetY: 10,
    // the types of items that allow the tooltip show up
    // 允许出现 tooltip 的 item 类型
    itemTypes: ['node', 'edge'],
    // custom the tooltip's content
    // 自定义 tooltip 内容
    getContent: (e) => {
      const outDiv = document.createElement('div');
      // outDiv.style.width = 'fit-content';
      outDiv.style.padding = '0px 40px 0px 20px';
      // node类型
      // {"id":"44269","n":"X-lab2017/open-digger","c":"r","i":25.29,"r":0.15,"v":24.81}
      function getCategory(c){
          switch (c){
            // 仓库
            case "r":
                return "repository"
            // 用户
            case "u":
                return "user"
            // issue
            case "i":
                return "issue"
            // pr
            default:
                return "pull request"
          }
      }
      if (e.item.getType() == 'node'){
        outDiv.innerHTML = `
        <h4>节点信息</h4>
        <ul>
            <li>ID: ${e.item.getModel().id}</li>
            <li>名称: ${e.item.getModel().n}</li>
            <li>类别: ${getCategory(e.item.getModel().c)}</li>
            <li>OpenRank值: ${e.item.getModel().v}</li>
        </ul>`;
      }
      // edge类型
      else if (e.item.getType() == 'edge'){
        outDiv.innerHTML = `
        <h4>边信息</h4>
        <ul>
          <li>起点ID: ${e.item.getModel().source}</li>
          <li>终点ID: ${e.item.getModel().target}</li>
          <li>边权重: ${e.item.getModel().weight}</li>
        </ul>
        `;
      }
      return outDiv;
    },
    shouldBegin: (e) => {
      // console.log(e.target);
      let res = true;
      switch (e.item.getModel().id) {
        case '1':
          res = false;
          break;
        case '2':
          if (e.target.get('name') === 'text-shape') res = true;
          else res = false;
          break;
        case '3':
          if (e.target.get('name') !== 'text-shape') res = true;
          else res = false;
          break;
        default:
          res = true;
          break;
      }
      return res;
    },
  });