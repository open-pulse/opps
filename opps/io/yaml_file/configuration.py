import yaml
import sys
import opps.model


class SafeDumperWithBlankLines(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) <= 2:
            super().write_line_break()
    
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)



# Constructors
def _complex_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> complex:
    return complex(**loader.construct_mapping(node))

def _point_constructor(loader: yaml.SafeLoader, node: yaml.nodes.MappingNode) -> opps.model.Point:
    return opps.model.Point(*loader.construct_sequence(node))

def _structure_multi_constructor(loader: yaml.SafeLoader, tag_suffix, node: yaml.nodes.MappingNode) -> opps.model.Structure:
    mapping = loader.construct_mapping(node)

    if tag_suffix == "Pipeline":
        p = opps.model.Pipeline()
        for key, val in mapping.items():
            setattr(p, key, val)
        return p

    subclass_name = tag_suffix
    structure_subclass = getattr(opps.model, subclass_name)
    return structure_subclass(**mapping)

# Representers
def _complex_representer(dumper: yaml.SafeDumper, obj: complex) -> yaml.nodes.MappingNode:
    return dumper.represent_mapping("!complex", {"real": obj.real, "imag": obj.imag})

def _point_representer(dumper: yaml.SafeDumper, obj: opps.model.Point) -> yaml.nodes.MappingNode:
    return dumper.represent_sequence("!Point", [float(i) for i in obj], flow_style=True) 

def _structure_multi_representer(dumper: yaml.SafeDumper, obj: opps.model.Structure) -> yaml.nodes.MappingNode:
    subclass_name = type(obj).__name__
    a = dumper.represent_mapping(f"!Structure.{subclass_name}", obj.as_dict())
    return a

def configure_custom_yaml():
    # Override library classes is not nice, but I think
    # that separating the items with a blank line is the 
    # correct behaviour.
    yaml.SafeDumper = SafeDumperWithBlankLines

    dumper = yaml.SafeDumper
    dumper.add_representer(complex, _complex_representer)
    dumper.add_representer(opps.model.Point, _point_representer)
    dumper.add_multi_representer(opps.model.Structure, _structure_multi_representer)

    loader = yaml.SafeLoader
    loader.add_constructor("!complex", _complex_constructor)
    loader.add_constructor("!Point", _point_constructor)
    loader.add_multi_constructor("!Structure.", _structure_multi_constructor)
