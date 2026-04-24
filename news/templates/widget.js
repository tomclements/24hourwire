(function() {
    'use strict';
    
    var config = {
        target: '{{ target|escapejs }}',
        theme: '{{ theme|escapejs }}',
        language: '{{ language|escapejs }}'
    };
    
    var stories = [
        {% for story in stories %}
        {
            title: '{{ story.title|escapejs }}',
            url: '{{ story.url|escapejs }}',
            source: '{{ story.source|escapejs }}',
            bias_label: '{{ story.bias_label|escapejs }}',
            image_url: '{{ story.image_url|escapejs }}'
        }{% if not forloop.last %},{% endif %}
        {% endfor %}
    ];
    
    var styles = {
        light: `
            .hourwire-widget { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 400px; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; background: #fff; }
            .hourwire-header { background: #0A2540; color: #fff; padding: 12px 16px; font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; gap: 8px; }
            .hourwire-header a { color: #fff; text-decoration: none; }
            .hourwire-header a:hover { text-decoration: underline; }
            .hourwire-story { padding: 12px 16px; border-bottom: 1px solid #f1f5f9; }
            .hourwire-story:last-child { border-bottom: none; }
            .hourwire-story-image { width: 100%; height: 120px; object-fit: cover; border-radius: 6px; margin-bottom: 8px; display: block; }
            .hourwire-story-title { font-size: 0.9rem; font-weight: 600; line-height: 1.4; margin: 0 0 6px 0; }
            .hourwire-story-title a { color: #1a1a1a; text-decoration: none; }
            .hourwire-story-title a:hover { color: #0066cc; }
            .hourwire-story-meta { display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: #64748b; }
            .hourwire-bias { padding: 1px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: 600; text-transform: uppercase; }
            .hourwire-bias.Left { background: #dbeafe; color: #2563eb; }
            .hourwire-bias.Left-Center { background: #eff6ff; color: #3b82f6; }
            .hourwire-bias.Center { background: #f3f4f6; color: #6b7280; }
            .hourwire-bias.Right-Center { background: #fef2f2; color: #ef4444; }
            .hourwire-bias.Right { background: #fee2e2; color: #dc2626; }
            .hourwire-footer { padding: 10px 16px; background: #f8fafc; border-top: 1px solid #e2e8f0; font-size: 0.75rem; text-align: center; }
            .hourwire-footer a { color: #0066cc; text-decoration: none; }
        `,
        dark: `
            .hourwire-widget { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 400px; border: 1px solid #334155; border-radius: 12px; overflow: hidden; background: #1e293b; }
            .hourwire-header { background: #0f172a; color: #f8fafc; padding: 12px 16px; font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; gap: 8px; }
            .hourwire-header a { color: #f8fafc; text-decoration: none; }
            .hourwire-story { padding: 12px 16px; border-bottom: 1px solid #334155; }
            .hourwire-story:last-child { border-bottom: none; }
            .hourwire-story-image { width: 100%; height: 120px; object-fit: cover; border-radius: 6px; margin-bottom: 8px; display: block; }
            .hourwire-story-title { font-size: 0.9rem; font-weight: 600; line-height: 1.4; margin: 0 0 6px 0; }
            .hourwire-story-title a { color: #f1f5f9; text-decoration: none; }
            .hourwire-story-title a:hover { color: #60a5fa; }
            .hourwire-story-meta { display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: #94a3b8; }
            .hourwire-bias { padding: 1px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: 600; text-transform: uppercase; }
            .hourwire-bias.Left { background: rgba(37,99,235,0.2); color: #60a5fa; }
            .hourwire-bias.Left-Center { background: rgba(59,130,246,0.15); color: #93c5fd; }
            .hourwire-bias.Center { background: rgba(107,114,128,0.2); color: #cbd5e1; }
            .hourwire-bias.Right-Center { background: rgba(239,68,68,0.15); color: #fca5a5; }
            .hourwire-bias.Right { background: rgba(220,38,38,0.2); color: #f87171; }
            .hourwire-footer { padding: 10px 16px; background: #0f172a; border-top: 1px solid #334155; font-size: 0.75rem; text-align: center; color: #94a3b8; }
            .hourwire-footer a { color: #60a5fa; text-decoration: none; }
        `
    };
    
    function renderWidget() {
        var container = document.querySelector(config.target);
        if (!container) {
            console.warn('24HourWire widget: target element "' + config.target + '" not found');
            return;
        }
        
        var html = '<div class="hourwire-widget">';
        html += '<div class="hourwire-header"><a href="https://24hourwire.news/?lang=' + config.language + '" target="_blank">24HourWire</a></div>';
        
        if (stories.length === 0) {
            html += '<div class="hourwire-story" style="text-align:center;color:#94a3b8;padding:20px;">No recent stories</div>';
        } else {
            stories.forEach(function(story) {
                html += '<div class="hourwire-story">';
                if (story.image_url) {
                    html += '<a href="' + story.url + '" target="_blank"><img src="' + story.image_url + '" alt="" class="hourwire-story-image" loading="lazy" onerror="this.style.display=\'none\'"></a>';
                }
                html += '<h3 class="hourwire-story-title"><a href="' + story.url + '" target="_blank">' + story.title + '</a></h3>';
                html += '<div class="hourwire-story-meta">';
                html += '<span>' + story.source + '</span>';
                if (story.bias_label && story.bias_label !== 'Unknown') {
                    html += '<span class="hourwire-bias ' + story.bias_label + '">' + story.bias_label + '</span>';
                }
                html += '</div>';
                html += '</div>';
            });
        }
        
        html += '<div class="hourwire-footer">News from all angles via <a href="https://24hourwire.news/?lang=' + config.language + '" target="_blank">24HourWire</a></div>';
        html += '</div>';
        
        container.innerHTML = html;
    }
    
    function injectStyles() {
        if (document.getElementById('hourwire-widget-styles')) return;
        var style = document.createElement('style');
        style.id = 'hourwire-widget-styles';
        style.textContent = styles[config.theme] || styles.light;
        document.head.appendChild(style);
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            injectStyles();
            renderWidget();
        });
    } else {
        injectStyles();
        renderWidget();
    }
})();
