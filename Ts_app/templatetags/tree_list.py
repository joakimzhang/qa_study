from django import template
register = template.Library()
from django.utils.safestring import SafeData, mark_safe

def li_tree(value):
    def walk_items(item_list):
        item_iterator = iter(item_list)
        try:
            item = next(item_iterator)
            
            while True:
                try:
                    next_item = next(item_iterator)
                except StopIteration:
                    yield item, None
                    break
                if not isinstance(next_item, tuple):
                    try:
                        iter(next_item)
                    except TypeError:
                        pass
                    else:
                        yield item, next_item
                        item = next(item_iterator)
                        continue
                yield item, None
                item = next_item
                
        except StopIteration:
            pass

    def list_formatter(item_list, tabs=1):
        indent = '\t' * tabs
        output = []
        for item, children in walk_items(item_list):
            sublist = ''
            if children:
                sublist = '\n%s<ul>\n%s\n%s</ul>\n%s' % (
                    indent, list_formatter(children, tabs + 1), indent, indent)
                #print item
                output.append('%s<li><font color="black"><a>%s</a>%s</li>' % (indent, item[0], sublist))
            else:
                output.append('%s<li><a href="/testcase/%s">%s</a>%s</li>' % (indent, item[1], item[0], sublist))    
        return '\n'.join(output)
    return mark_safe(list_formatter(value))

register.filter("li_tree", li_tree)