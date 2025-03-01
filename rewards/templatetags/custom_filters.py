from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    # 辞書から指定したキーの値を取得するカスタムフィルター
    # 例: {{ my_dict|get_item:my_key }}
    return dictionary.get(str(key), [])