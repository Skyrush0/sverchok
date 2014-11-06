# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

old_bl_idnames = {
#    'BakeryNode' : "bakery",
    'CircleNode' : "circle",
    'ListItemNode' : "list_item",
    'GenRangeNode' : "range",
    'GenSeriesNode' : "series",
#    'Test1Node' : "test",
#    'Test2Node' : "test",
#    'ToolsNode' : "tools",
    'SvReRouteNode': "reroute",
    'VoronoiNode': "voronoi",
    'ViewerNode': "viewer",
    'EvalKnievalNode': "eval_knieval",
    'FormulaNode': 'formula',
}

# we should add some functions to load things there
import importlib
import inspect
import traceback

import bpy

from sverchok.node_tree import SverchCustomTreeNode
imported_mods = {}

def load_old(ng):
    
    """
    This approach didn't work, bl_idname of undefined node isn't as I expected
    bl_idnames = {n.bl_idname for n in ng.nodes} 
    old_bl_ids = bl_idnames.intersection(old_bl_idnames)
    if old_bl_ids:
    
    """
    not_reged_nodes = list(n for n in ng.nodes if not n.is_registered_node_type())
    if not_reged_nodes:
        for bl_id in old_bl_idnames:
            register_old(bl_id)
            nodes = [n for n in ng.nodes if n.bl_idname == bl_id]
            if nodes:
                for node in nodes:
                    frame = ng.nodes.new("NodeFrame")
                    if node.parent:
                        frame.parent = node.parent
                    node.parent = frame
                    frame.label = "Deprecated node!"
                    frame.use_custom_color = True
                    frame.color = (.8, 0, 0)
                    frame.shrink = True
                not_reged_nodes = list(n for n in ng.nodes if not n.is_registered_node_type())
                node_count = len(not_reged_nodes)
                print("Loaded {}. {} nodes are left unregisted.".format(bl_id, node_count))
                if node_count == 0:
                    return
            else: # didn't help remove
                unregister_old(bl_id)
    
def register_old(bl_id):
    if bl_id in old_bl_idnames:
        mod = importlib.import_module(".{}".format(old_bl_idnames[bl_id]), __name__)
        res = inspect.getmembers(mod)
        for name, cls in res:
            if inspect.isclass(cls):
                if issubclass(cls, bpy.types.Node) and cls.bl_idname == bl_id:
                    if bl_id not in imported_mods:
                        try:
                            mod.register()
                        except:
                            traceback.print_exc()
                        imported_mods[bl_id] = mod
                        return mod
                    
    print("Cannot find {} among old nodes".format(bl_id))

def unregister_old(bl_id):
    mod = imported_mods.get(bl_id)
    if mod:
        #print("Unloaded old node type {}".format(bl_id)) 
        mod.unregister()
        del imported_mods[bl_id]
         
def unregister():
    for mod in imported_mods.values():
        mod.unregister()
        
