import setuptools  # 导入setuptools打包工具

with open(r"F:\please_package\README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crawles",  # 用自己的名替换其中的YOUR_USERNAME_
    version="0.4.1",  # 包版本号，便于维护版本
    author="苯环",  # 作者，可以写自己的姓名
    author_email="1431705288@qq.com",  # 作者联系方式，可写自己的邮箱地址
    description="这是一个简单的爬虫封装模块，封装一些请求优化与下载功能",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://github.com/kuangjianke/crawles",  # 自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    install_requires=[
        'aiofiles',  # 异步图片
        'aiohttp',  # 异步请求
        'pyexecjs',  # js 代码运行
        'lxml',  # 解析模块
        'jinja2',  # 模标
        'objprint',  # 打印模块
        'requests',  # 请求模块
        'curl_cffi',  # 请求模块
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',  # 对python的最低版本要求
)

# 用setup.py打包项目
# python F:\please_package\setup.py sdist bdist_wheel
# 上传项目
# python -m twine upload dist/* -u 1431705288qq.com -p a13641481495

# python -m twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDc1ZWFkNjAzLWE1ZmQtNDY4MC04NGRiLWQ1M2E4MjY5Njc1NwACD1sxLFsiY3Jhd2xlcyJdXQACLFsyLFsiMmI5NDA5ZjYtNjJiOS00YThlLThhYjgtYWY2YTAxMWJkZjk0Il1dAAAGIIKxso3j5CIUSJErC5ONmnB2EYbi5L-BOmhdu5yHXNwj
# 输入账号密码完成上传
# 1431705288qq.com
# a13641481495
# https://upload.pypi.org/legacy/
'''
kjk_crawles

pypi-AgEIcHlwaS5vcmcCJDc1ZWFkNjAzLWE1ZmQtNDY4MC04NGRiLWQ1M2E4MjY5Njc1NwACD1sxLFsiY3Jhd2xlcyJdXQACLFsyLFsiMmI5NDA5ZjYtNjJiOS00YThlLThhYjgtYWY2YTAxMWJkZjk0Il1dAAAGIIKxso3j5CIUSJErC5ONmnB2EYbi5L-BOmhdu5yHXNwj


InvalidConfiguration: Missing 'crawles.pypirc' section from ~/.pypirc.
         More info: https://packaging.python.org/specifications/pypirc/
'''