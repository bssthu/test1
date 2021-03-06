#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : main.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 
# 


import os
import sys
import shutil
import time
import zipfile

sys.path.insert(0, '../../scripts/')
from utils import log
from utils.xlsutils import load_xls


def execute(cmd):
    print('> %s' % cmd)
    ret = os.system(cmd)
    if ret != 0:
        sys.exit(-1)


def get_linenum(filename):
    with open(filename, 'rt', encoding='utf-8') as fp:
        return len(fp.readlines())


def gen_chs():
    """1. 简体"""
    NEED_CLEAR = True
    log.info(os.getcwd())

    if NEED_CLEAR:
        print('### 正在清理...')
        log.debug('正在清理...')
        # 清理输出目录
        dirs = (
            '../../输出/生成简体插件/',
        )
        for dir in dirs:
            if os.path.exists(dir):
                log.info('clear %s' % dir)
                shutil.rmtree(dir)
        # 清理翻译中间目录
        log.info('clear csv and xlsx')
        for root, dirs, files in os.walk('../../translation/lang/translated/'):
            for f in files:
                if f.endswith('.csv') or f.endswith('.xlsx') or f.endswith('.lang'):
                    filename = os.path.join(root, f)
                    log.debug('remove %s' % filename)
                    os.remove(filename)
            break
        for root, dirs, files in os.walk('../../translation/'):
            for f in files:
                if f.endswith('.csv') or f.endswith('.xlsx'):
                    filename = os.path.join(root, f)
                    log.debug('remove %s' % filename)
                    os.remove(filename)
            break
        files = (
            '../../translation/zh_translate.txt',
            '../../translation/zh_translate.xlsx',
        )
        for f in files:
            if os.path.exists(f):
                log.debug('remove %s' % f)
                os.remove(f)

    print('### 创建目录...')
    log.debug('创建目录...')
    dirs = (
        '../../输出/生成简体插件/',
    )
    for dir in dirs:
        if not os.path.isdir(dir):
            log.info('create %s' % dir)
            os.makedirs(dir)

    print('### 拷贝文件...')
    log.debug('拷贝文件...')
    for root, dirs, files in os.walk('汉化xlsx/'):
        for f in files:
            if f.endswith('.xlsx') and not f.startswith('~'):
                filename = os.path.join(root, f)
                data = load_xls(filename)
                if len(data[1]) == 8:  # ui 汉化文件
                    dst = '../../translation/'
                    ui_xls_file = f
                    log.info('copy %s to %s' % (filename, dst))
                    shutil.copy(filename, dst)
                dst = '../../translation/lang/translated/'
                log.info('copy %s to %s' % (filename, dst))
                shutil.copy(filename, dst)

    os.chdir('../../scripts/')
    log.info(os.getcwd())
    print('### 转换UI文本...')
    log.debug('转换UI文本...')
    execute('python export_uixls_to_txt.py ../translation/%s' % ui_xls_file)
    execute('python convert_txt_to_str.py -m translation')

    print('### 转换其他文本...')
    log.debug('转换其他文本...')
    execute('python export_langxls_to_csv.py')

    os.chdir('../translation/lang/translated/')
    log.info(os.getcwd())
    print('### 正在编码...')
    log.debug('正在编码...')
    execute('EsoExtractData.exe -x zh.lang.csv')

    print('### 正在校验...')
    log.debug('正在校验...')
    shutil.copy('zh.lang', 'zh1.lang')
    execute('EsoExtractData -l zh1.lang')
    num1 = get_linenum('../en.lang.csv')
    num2 = get_linenum('zh.lang.csv')
    num3 = get_linenum('zh1.lang.csv')
    log.info('validate line num: %d, %d, %d' % (num1, num2, num3))
    if not num1 == num2 == num3:
        log.error('校验失败')
        sys.exit(-1)

    os.chdir('../../../')
    log.info(os.getcwd())
    print('### 正在打包...')
    log.debug('正在打包...')
    log.info('copy AddOns')
    shutil.copytree('AddOns/', '输出/生成简体插件/AddOns')
    log.info('copy lang')
    shutil.copy('translation/lang/translated/zh.lang', '输出/生成简体插件/AddOns/gamedata/lang/')
    log.info('copy readme')
    shutil.copy('工具/生成插件/README_chs.txt', '输出/生成简体插件/README.txt')
    log.info('clear AddOns')
    os.remove('输出/生成简体插件/AddOns/EsoUI/lang/.gitignore')
    os.remove('输出/生成简体插件/AddOns/EsoZH/fonts/README.md')
    os.remove('输出/生成简体插件/AddOns/gamedata/lang/.gitignore')

    os.chdir('输出/生成简体插件/')
    log.info(os.getcwd())
    with open('README.txt', 'rt', encoding='utf-8') as fp:
        desc = fp.read()
    zip_name = 'ESO汉化插件.zip'
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    zipf.comment = bytes(desc, encoding='gbk')
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f != zip_name:
                zipf.write(os.path.join(root, f))
    zipf.close()


def gen_cht():
    """2. 繁体"""
    NEED_CLEAR = True
    log.info(os.getcwd())

    if NEED_CLEAR:
        print('### 正在清理...')
        log.debug('正在清理...')
        # 清理输出目录
        dirs = (
            '../../输出/生成繁体插件/',
        )
        for dir in dirs:
            if os.path.exists(dir):
                log.info('clear %s' % dir)
                shutil.rmtree(dir)
        # 清理翻译中间目录
        files = (
            '../../translation/STOthers.txt',
            '../../translation/lang/translated/cht/zh_pregame.str',
            '../../translation/lang/translated/cht/zh_client.str',
            '../../translation/lang/translated/cht/zh.lang',
            '../../translation/lang/translated/cht/zh.lang.csv',
            '../../translation/lang/translated/zh1.lang',
            '../../translation/lang/translated/zh1.lang.csv',
        )
        for f in files:
            if os.path.exists(f):
                log.debug('remove %s' % f)
                os.remove(f)
        for root, dirs, files in os.walk('../../translation/'):
            for f in files:
                if f.endswith('.xlsx'):
                    filename = os.path.join(root, f)
                    log.debug('remove %s' % filename)
                    os.remove(filename)
            break

    print('### 创建目录...')
    log.debug('创建目录...')
    dirs = (
        '../../输出/生成繁体插件/',
    )
    for dir in dirs:
        if not os.path.isdir(dir):
            log.info('create %s' % dir)
            os.makedirs(dir)

    print('### 分析对照表...')
    log.debug('分析对照表...')
    for root, dirs, files in os.walk('简繁对照'):
        for f in files:
            if f.endswith('.xlsx') and not f.startswith('~'):
                filename = os.path.join(root, f)
                dst = '../../translation/'
                log.info('copy %s to %s', filename, dst)
                shutil.copy(filename, dst)
                chs_to_cht_file = f
                break

    os.chdir('../../translation/')
    log.info(os.getcwd())
    execute('python ../scripts/xls2csv.py "%s" STOthers.txt' % chs_to_cht_file)
    with open('STOthers.txt', 'rt', encoding='utf-8') as fp:
        lines = fp.readlines()
    with open('STOthers.txt', 'wt', encoding='utf-8') as fp:
        fp.write(''.join(lines[1:]))

    os.chdir('../scripts/')
    log.info(os.getcwd())
    print('### 简繁转换...')
    log.debug('简繁转换...')
    src_dst = (
        ('../AddOns/EsoUI/lang/zh_pregame.str', '../translation/lang/translated/cht/zh_pregame.str',),
        ('../AddOns/EsoUI/lang/zh_client.str', '../translation/lang/translated/cht/zh_client.str',),
        ('../translation/lang/translated/zh.lang.csv', '../translation/lang/translated/cht/zh.lang.csv',),
    )
    for src, dst in src_dst:
        execute('python convert_to_cht.py %s %s' % (src, dst))

    os.chdir('../translation/lang/translated/')
    log.info(os.getcwd())
    print('### 正在编码...')
    log.debug('正在编码...')
    execute('EsoExtractData.exe -x cht/zh.lang.csv')

    print('### 正在校验...')
    log.debug('正在校验...')
    shutil.copy('cht/zh.lang', 'zh1.lang')
    execute('EsoExtractData -l zh1.lang')
    num1 = get_linenum('../en.lang.csv')
    num2 = get_linenum('cht/zh.lang.csv')
    num3 = get_linenum('zh1.lang.csv')
    log.info('validate line num: %d, %d, %d' % (num1, num2, num3))
    if not num1 == num2 == num3:
        log.error('校验失败')
        sys.exit(-1)

    os.chdir('../../../')
    log.info(os.getcwd())
    print('### 正在打包...')
    log.debug('正在打包...')
    log.info('copy AddOns')
    shutil.copytree('AddOns/', '输出/生成繁体插件/AddOns')
    log.info('copy lang')
    shutil.copy('translation/lang/translated/cht/zh.lang', '输出/生成繁体插件/AddOns/gamedata/lang/')
    shutil.copy('translation/lang/translated/cht/zh_pregame.str', '输出/生成繁体插件/AddOns//EsoUI/lang/')
    shutil.copy('translation/lang/translated/cht/zh_client.str', '输出/生成繁体插件/AddOns//EsoUI/lang/')
    log.info('copy fonts')
    shutil.rmtree('输出/生成繁体插件/AddOns/EsoZH/fonts/')
    shutil.copytree('translation/lang/translated/cht/fonts/', '输出/生成繁体插件/AddOns/EsoZH/fonts/')
    log.info('copy readme')
    shutil.copy('工具/生成插件/README_cht.txt', '输出/生成繁体插件/README.txt')
    log.info('clear AddOns')
    os.remove('输出/生成繁体插件/AddOns/EsoUI/lang/.gitignore')
    os.remove('输出/生成繁体插件/AddOns/gamedata/lang/.gitignore')

    os.chdir('输出/生成繁体插件/')
    log.info(os.getcwd())
    with open('README.txt', 'rt', encoding='utf-8') as fp:
        desc = fp.read()
    zip_name = 'ESO汉化插件_繁体.zip'
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    zipf.comment = bytes(desc, encoding='gbk')
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f != zip_name:
                zipf.write(os.path.join(root, f))
    zipf.close()


def gen_chs_force():
    """3. 强制简体，用原版做一次繁简转换"""
    NEED_CLEAR = True
    log.info(os.getcwd())

    if NEED_CLEAR:
        print('### 正在清理...')
        log.debug('正在清理...')
        # 清理输出目录
        dirs = (
            '../../输出/生成简体插件/',
        )
        for dir in dirs:
            if os.path.exists(dir):
                log.info('clear %s' % dir)
                shutil.rmtree(dir)
        # 清理翻译中间目录
        files = (
            '../../translation/STOthers_ts.txt',
            '../../translation/lang/translated/zh1.lang',
            '../../translation/lang/translated/zh1.lang.csv',
        )
        for f in files:
            if os.path.exists(f):
                log.debug('remove %s' % f)
                os.remove(f)
        for root, dirs, files in os.walk('../../translation/'):
            for f in files:
                if f.endswith('.xlsx'):
                    filename = os.path.join(root, f)
                    log.debug('remove %s' % filename)
                    os.remove(filename)
            break

    print('### 创建目录...')
    log.debug('创建目录...')
    dirs = (
        '../../输出/生成简体插件/',
    )
    for dir in dirs:
        if not os.path.isdir(dir):
            log.info('create %s' % dir)
            os.makedirs(dir)

    print('### 分析对照表...')
    log.debug('分析对照表...')
    for root, dirs, files in os.walk('繁简对照'):
        for f in files:
            if f.endswith('.xlsx') and not f.startswith('~'):
                filename = os.path.join(root, f)
                dst = '../../translation/'
                log.info('copy %s to %s', filename, dst)
                shutil.copy(filename, dst)
                cht_to_chs_file = f
                break

    os.chdir('../../translation/')
    log.info(os.getcwd())
    execute('python ../scripts/xls2csv.py "%s" STOthers_ts.txt' % cht_to_chs_file)
    with open('STOthers_ts.txt', 'rt', encoding='utf-8') as fp:
        lines = fp.readlines()
    with open('STOthers_ts.txt', 'wt', encoding='utf-8') as fp:
        fp.write(''.join(lines[1:]))

    os.chdir('../scripts/')
    log.info(os.getcwd())
    print('### 繁简转换...')
    log.debug('繁简转换...')
    # 直接覆盖吧
    src_dst = (
        ('../AddOns/EsoUI/lang/zh_pregame.str', '../AddOns/EsoUI/lang/zh_pregame.str',),
        ('../AddOns/EsoUI/lang/zh_client.str', '../AddOns/EsoUI/lang/zh_client.str',),
        ('../translation/lang/translated/zh.lang.csv', '../translation/lang/translated/zh.lang.csv',),
    )
    for src, dst in src_dst:
        execute('python convert_to_chs.py %s %s' % (src, dst))

    os.chdir('../translation/lang/translated/')
    log.info(os.getcwd())
    print('### 正在编码...')
    log.debug('正在编码...')
    execute('EsoExtractData.exe -x zh.lang.csv')

    print('### 正在校验...')
    log.debug('正在校验...')
    shutil.copy('zh.lang', 'zh1.lang')
    execute('EsoExtractData -l zh1.lang')
    num1 = get_linenum('../en.lang.csv')
    num2 = get_linenum('zh.lang.csv')
    num3 = get_linenum('zh1.lang.csv')
    log.info('validate line num: %d, %d, %d' % (num1, num2, num3))
    if not num1 == num2 == num3:
        log.error('校验失败')
        sys.exit(-1)

    os.chdir('../../../')
    log.info(os.getcwd())
    print('### 正在打包...')
    log.debug('正在打包...')
    log.info('copy AddOns')
    shutil.copytree('AddOns/', '输出/生成简体插件/AddOns')
    log.info('copy lang')
    shutil.copy('translation/lang/translated/zh.lang', '输出/生成简体插件/AddOns/gamedata/lang/')
    log.info('copy readme')
    shutil.copy('工具/生成插件/README_chs.txt', '输出/生成简体插件/README.txt')
    log.info('clear AddOns')
    os.remove('输出/生成简体插件/AddOns/EsoUI/lang/.gitignore')
    os.remove('输出/生成简体插件/AddOns/EsoZH/fonts/README.md')
    os.remove('输出/生成简体插件/AddOns/gamedata/lang/.gitignore')

    os.chdir('输出/生成简体插件/')
    log.info(os.getcwd())
    with open('README.txt', 'rt', encoding='utf-8') as fp:
        desc = fp.read()
    zip_name = 'ESO汉化插件.zip'
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    zipf.comment = bytes(desc, encoding='gbk')
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f != zip_name:
                zipf.write(os.path.join(root, f))
    zipf.close()


def main():
    if sys.argv[1] == '1':
        gen_chs()
    elif sys.argv[1] == '2':
        gen_cht()
    elif sys.argv[1] == '3':
        gen_chs_force()
    else:
        log.warning('unknown args')
        sys.exit(-2)


if __name__ == '__main__':
    log.debug('main() with args: %s' % str(sys.argv))
    main()
