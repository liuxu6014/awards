// 主JavaScript文件

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 设置当前年份
    document.querySelectorAll('.current-year').forEach(function(el) {
        el.textContent = new Date().getFullYear();
    });
    
    // 表格排序功能
    document.querySelectorAll('.sortable').forEach(function(table) {
        setupTableSort(table);
    });
    
    // 自动关闭警告消息
    setTimeout(function() {
        document.querySelectorAll('.alert-dismissible').forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// 表格排序功能
function setupTableSort(table) {
    var headers = table.querySelectorAll('th');
    headers.forEach(function(header, index) {
        if (!header.classList.contains('no-sort')) {
            header.addEventListener('click', function() {
                sortTable(table, index);
            });
            header.style.cursor = 'pointer';
            header.title = '点击排序';
        }
    });
}

// 排序表格
function sortTable(table, columnIndex) {
    var rows = Array.from(table.querySelectorAll('tbody tr'));
    var header = table.querySelectorAll('th')[columnIndex];
    var isAscending = header.classList.contains('sort-asc');
    
    // 清除所有排序标记
    table.querySelectorAll('th').forEach(function(th) {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    // 设置新的排序标记
    header.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
    
    // 排序行
    rows.sort(function(rowA, rowB) {
        var cellA = rowA.querySelectorAll('td')[columnIndex].textContent.trim();
        var cellB = rowB.querySelectorAll('td')[columnIndex].textContent.trim();
        
        // 尝试数字排序
        var numA = parseFloat(cellA);
        var numB = parseFloat(cellB);
        
        if (!isNaN(numA) && !isNaN(numB)) {
            return isAscending ? numB - numA : numA - numB;
        }
        
        // 字符串排序
        return isAscending ? 
            cellB.localeCompare(cellA, 'zh-CN') : 
            cellA.localeCompare(cellB, 'zh-CN');
    });
    
    // 重新添加排序后的行
    var tbody = table.querySelector('tbody');
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
}

// 格式化日期
function formatDate(dateStr) {
    if (!dateStr) return '';
    var date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr;
    
    return date.getFullYear() + '-' + 
           padZero(date.getMonth() + 1) + '-' + 
           padZero(date.getDate()) + ' ' + 
           padZero(date.getHours()) + ':' + 
           padZero(date.getMinutes());
}

// 数字补零
function padZero(num) {
    return num < 10 ? '0' + num : num;
}

// 复制到剪贴板
function copyToClipboard(text) {
    var textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    
    // 显示提示
    showToast('已复制到剪贴板');
}

// 显示提示消息
function showToast(message, type = 'success') {
    var toast = document.createElement('div');
    toast.className = 'toast align-items-center text-white bg-' + type;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    var container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    container.appendChild(toast);
    var bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // 自动移除
    toast.addEventListener('hidden.bs.toast', function() {
        container.removeChild(toast);
    });
} 