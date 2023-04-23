from flask import Flask, render_template, request
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from jinja2 import Markup

app = Flask(__name__)


def bar_base(n: int = 10):
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [n, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 30, 18,65, 70])
        .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
        # 或者直接使用字典参数
        # .set_global_opts(title_opts={"text": "主标题", "subtext": "副标题"})
    )
    return bar 

@app.route('/', methods=['GET','POST'])
def index():
    args = request.args 
    n = args.get('n',10, type=int)
    bar = bar_base(n)
    return Markup(bar.render_embed())


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
