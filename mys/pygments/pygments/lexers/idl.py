"""
    pygments.lexers.idl
    ~~~~~~~~~~~~~~~~~~~

    Lexers for IDL.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer
from pygments.lexer import words
from pygments.token import Comment
from pygments.token import Keyword
from pygments.token import Name
from pygments.token import Number
from pygments.token import Operator
from pygments.token import String
from pygments.token import Text

__all__ = ['IDLLexer']


class IDLLexer(RegexLexer):
    """
    Pygments Lexer for IDL (Interactive Data Language).

    .. versionadded:: 1.6
    """
    name = 'IDL'
    aliases = ['idl']
    filenames = ['*.pro']
    mimetypes = ['text/idl']

    flags = re.IGNORECASE | re.MULTILINE

    _RESERVED = (
        'and', 'begin', 'break', 'case', 'common', 'compile_opt',
        'continue', 'do', 'else', 'end', 'endcase', 'endelse',
        'endfor', 'endforeach', 'endif', 'endrep', 'endswitch',
        'endwhile', 'eq', 'for', 'foreach', 'forward_function',
        'function', 'ge', 'goto', 'gt', 'if', 'inherits', 'le',
        'lt', 'mod', 'ne', 'not', 'of', 'on_ioerror', 'or', 'pro',
        'repeat', 'switch', 'then', 'until', 'while', 'xor')
    """Reserved words from: http://www.exelisvis.com/docs/reswords.html"""

    _BUILTIN_LIB = (
        'abs', 'acos', 'adapt_hist_equal', 'alog', 'alog10',
        'amoeba', 'annotate', 'app_user_dir', 'app_user_dir_query',
        'arg_present', 'array_equal', 'array_indices', 'arrow',
        'ascii_template', 'asin', 'assoc', 'atan', 'axis',
        'a_correlate', 'bandpass_filter', 'bandreject_filter',
        'barplot', 'bar_plot', 'beseli', 'beselj', 'beselk',
        'besely', 'beta', 'bilinear', 'binary_template', 'bindgen',
        'binomial', 'bin_date', 'bit_ffs', 'bit_population',
        'blas_axpy', 'blk_con', 'box_cursor', 'breakpoint',
        'broyden', 'butterworth', 'bytarr', 'byte', 'byteorder',
        'bytscl', 'caldat', 'calendar', 'call_external',
        'call_function', 'call_method', 'call_procedure', 'canny',
        'catch', 'cd', r'cdf_\w*', 'ceil', 'chebyshev',
        'check_math',
        'chisqr_cvf', 'chisqr_pdf', 'choldc', 'cholsol', 'cindgen',
        'cir_3pnt', 'close', 'cluster', 'cluster_tree', 'clust_wts',
        'cmyk_convert', 'colorbar', 'colorize_sample',
        'colormap_applicable', 'colormap_gradient',
        'colormap_rotation', 'colortable', 'color_convert',
        'color_exchange', 'color_quan', 'color_range_map', 'comfit',
        'command_line_args', 'complex', 'complexarr', 'complexround',
        'compute_mesh_normals', 'cond', 'congrid', 'conj',
        'constrained_min', 'contour', 'convert_coord', 'convol',
        'convol_fft', 'coord2to3', 'copy_lun', 'correlate', 'cos',
        'cosh', 'cpu', 'cramer', 'create_cursor', 'create_struct',
        'create_view', 'crossp', 'crvlength', 'cti_test',
        'ct_luminance', 'cursor', 'curvefit', 'cvttobm', 'cv_coord',
        'cw_animate', 'cw_animate_getp', 'cw_animate_load',
        'cw_animate_run', 'cw_arcball', 'cw_bgroup', 'cw_clr_index',
        'cw_colorsel', 'cw_defroi', 'cw_field', 'cw_filesel',
        'cw_form', 'cw_fslider', 'cw_light_editor',
        'cw_light_editor_get', 'cw_light_editor_set', 'cw_orient',
        'cw_palette_editor', 'cw_palette_editor_get',
        'cw_palette_editor_set', 'cw_pdmenu', 'cw_rgbslider',
        'cw_tmpl', 'cw_zoom', 'c_correlate', 'dblarr', 'db_exists',
        'dcindgen', 'dcomplex', 'dcomplexarr', 'define_key',
        'define_msgblk', 'define_msgblk_from_file', 'defroi',
        'defsysv', 'delvar', 'dendrogram', 'dendro_plot', 'deriv',
        'derivsig', 'determ', 'device', 'dfpmin', 'diag_matrix',
        'dialog_dbconnect', 'dialog_message', 'dialog_pickfile',
        'dialog_printersetup', 'dialog_printjob',
        'dialog_read_image', 'dialog_write_image', 'digital_filter',
        'dilate', 'dindgen', 'dissolve', 'dist', 'distance_measure',
        'dlm_load', 'dlm_register', 'doc_library', 'double',
        'draw_roi', 'edge_dog', 'efont', 'eigenql', 'eigenvec',
        'ellipse', 'elmhes', 'emboss', 'empty', 'enable_sysrtn',
        'eof', r'eos_\w*', 'erase', 'erf', 'erfc', 'erfcx',
        'erode', 'errorplot', 'errplot', 'estimator_filter',
        'execute', 'exit', 'exp', 'expand', 'expand_path', 'expint',
        'extrac', 'extract_slice', 'factorial', 'fft', 'filepath',
        'file_basename', 'file_chmod', 'file_copy', 'file_delete',
        'file_dirname', 'file_expand_path', 'file_info',
        'file_lines', 'file_link', 'file_mkdir', 'file_move',
        'file_poll_input', 'file_readlink', 'file_same',
        'file_search', 'file_test', 'file_which', 'findgen',
        'finite', 'fix', 'flick', 'float', 'floor', 'flow3',
        'fltarr', 'flush', 'format_axis_values', 'free_lun',
        'fstat', 'fulstr', 'funct', 'fv_test', 'fx_root',
        'fz_roots', 'f_cvf', 'f_pdf', 'gamma', 'gamma_ct',
        'gauss2dfit', 'gaussfit', 'gaussian_function', 'gaussint',
        'gauss_cvf', 'gauss_pdf', 'gauss_smooth', 'getenv',
        'getwindows', 'get_drive_list', 'get_dxf_objects',
        'get_kbrd', 'get_login_info', 'get_lun', 'get_screen_size',
        'greg2jul', r'grib_\w*', 'grid3', 'griddata',
        'grid_input', 'grid_tps', 'gs_iter',
        r'h5[adfgirst]_\w*', 'h5_browser', 'h5_close',
        'h5_create', 'h5_get_libversion', 'h5_open', 'h5_parse',
        'hanning', 'hash', r'hdf_\w*', 'heap_free',
        'heap_gc', 'heap_nosave', 'heap_refcount', 'heap_save',
        'help', 'hilbert', 'histogram', 'hist_2d', 'hist_equal',
        'hls', 'hough', 'hqr', 'hsv', 'h_eq_ct', 'h_eq_int',
        'i18n_multibytetoutf8', 'i18n_multibytetowidechar',
        'i18n_utf8tomultibyte', 'i18n_widechartomultibyte',
        'ibeta', 'icontour', 'iconvertcoord', 'idelete', 'identity',
        'idlexbr_assistant', 'idlitsys_createtool', 'idl_base64',
        'idl_validname', 'iellipse', 'igamma', 'igetcurrent',
        'igetdata', 'igetid', 'igetproperty', 'iimage', 'image',
        'image_cont', 'image_statistics', 'imaginary', 'imap',
        'indgen', 'intarr', 'interpol', 'interpolate',
        'interval_volume', 'int_2d', 'int_3d', 'int_tabulated',
        'invert', 'ioctl', 'iopen', 'iplot', 'ipolygon',
        'ipolyline', 'iputdata', 'iregister', 'ireset', 'iresolve',
        'irotate', 'ir_filter', 'isa', 'isave', 'iscale',
        'isetcurrent', 'isetproperty', 'ishft', 'isocontour',
        'isosurface', 'isurface', 'itext', 'itranslate', 'ivector',
        'ivolume', 'izoom', 'i_beta', 'journal', 'json_parse',
        'json_serialize', 'jul2greg', 'julday', 'keyword_set',
        'krig2d', 'kurtosis', 'kw_test', 'l64indgen', 'label_date',
        'label_region', 'ladfit', 'laguerre', 'laplacian',
        'la_choldc', 'la_cholmprove', 'la_cholsol', 'la_determ',
        'la_eigenproblem', 'la_eigenql', 'la_eigenvec', 'la_elmhes',
        'la_gm_linear_model', 'la_hqr', 'la_invert',
        'la_least_squares', 'la_least_square_equality',
        'la_linear_equation', 'la_ludc', 'la_lumprove', 'la_lusol',
        'la_svd', 'la_tridc', 'la_trimprove', 'la_triql',
        'la_trired', 'la_trisol', 'least_squares_filter', 'leefilt',
        'legend', 'legendre', 'linbcg', 'lindgen', 'linfit',
        'linkimage', 'list', 'll_arc_distance', 'lmfit', 'lmgr',
        'lngamma', 'lnp_test', 'loadct', 'locale_get',
        'logical_and', 'logical_or', 'logical_true', 'lon64arr',
        'lonarr', 'long', 'long64', 'lsode', 'ludc', 'lumprove',
        'lusol', 'lu_complex', 'machar', 'make_array', 'make_dll',
        'make_rt', 'map', 'mapcontinents', 'mapgrid', 'map_2points',
        'map_continents', 'map_grid', 'map_image', 'map_patch',
        'map_proj_forward', 'map_proj_image', 'map_proj_info',
        'map_proj_init', 'map_proj_inverse', 'map_set',
        'matrix_multiply', 'matrix_power', 'max', 'md_test',
        'mean', 'meanabsdev', 'mean_filter', 'median', 'memory',
        'mesh_clip', 'mesh_decimate', 'mesh_issolid', 'mesh_merge',
        'mesh_numtriangles', 'mesh_obj', 'mesh_smooth',
        'mesh_surfacearea', 'mesh_validate', 'mesh_volume',
        'message', 'min', 'min_curve_surf', 'mk_html_help',
        'modifyct', 'moment', 'morph_close', 'morph_distance',
        'morph_gradient', 'morph_hitormiss', 'morph_open',
        'morph_thin', 'morph_tophat', 'multi', 'm_correlate',
        r'ncdf_\w*', 'newton', 'noise_hurl', 'noise_pick',
        'noise_scatter', 'noise_slur', 'norm', 'n_elements',
        'n_params', 'n_tags', 'objarr', 'obj_class', 'obj_destroy',
        'obj_hasmethod', 'obj_isa', 'obj_new', 'obj_valid',
        'online_help', 'on_error', 'open', 'oplot', 'oploterr',
        'parse_url', 'particle_trace', 'path_cache', 'path_sep',
        'pcomp', 'plot', 'plot3d', 'ploterr', 'plots', 'plot_3dbox',
        'plot_field', 'pnt_line', 'point_lun', 'polarplot',
        'polar_contour', 'polar_surface', 'poly', 'polyfill',
        'polyfillv', 'polygon', 'polyline', 'polyshade', 'polywarp',
        'poly_2d', 'poly_area', 'poly_fit', 'popd', 'powell',
        'pref_commit', 'pref_get', 'pref_set', 'prewitt', 'primes',
        'print', 'printd', 'product', 'profile', 'profiler',
        'profiles', 'project_vol', 'psafm', 'pseudo',
        'ps_show_fonts', 'ptrarr', 'ptr_free', 'ptr_new',
        'ptr_valid', 'pushd', 'p_correlate', 'qgrid3', 'qhull',
        'qromb', 'qromo', 'qsimp', 'query_ascii', 'query_bmp',
        'query_csv', 'query_dicom', 'query_gif', 'query_image',
        'query_jpeg', 'query_jpeg2000', 'query_mrsid', 'query_pict',
        'query_png', 'query_ppm', 'query_srf', 'query_tiff',
        'query_wav', 'radon', 'randomn', 'randomu', 'ranks',
        'rdpix', 'read', 'reads', 'readu', 'read_ascii',
        'read_binary', 'read_bmp', 'read_csv', 'read_dicom',
        'read_gif', 'read_image', 'read_interfile', 'read_jpeg',
        'read_jpeg2000', 'read_mrsid', 'read_pict', 'read_png',
        'read_ppm', 'read_spr', 'read_srf', 'read_sylk',
        'read_tiff', 'read_wav', 'read_wave', 'read_x11_bitmap',
        'read_xwd', 'real_part', 'rebin', 'recall_commands',
        'recon3', 'reduce_colors', 'reform', 'region_grow',
        'register_cursor', 'regress', 'replicate',
        'replicate_inplace', 'resolve_all', 'resolve_routine',
        'restore', 'retall', 'return', 'reverse', 'rk4', 'roberts',
        'rot', 'rotate', 'round', 'routine_filepath',
        'routine_info', 'rs_test', 'r_correlate', 'r_test',
        'save', 'savgol', 'scale3', 'scale3d', 'scope_level',
        'scope_traceback', 'scope_varfetch', 'scope_varname',
        'search2d', 'search3d', 'sem_create', 'sem_delete',
        'sem_lock', 'sem_release', 'setenv', 'set_plot',
        'set_shading', 'sfit', 'shade_surf', 'shade_surf_irr',
        'shade_volume', 'shift', 'shift_diff', 'shmdebug', 'shmmap',
        'shmunmap', 'shmvar', 'show3', 'showfont', 'simplex', 'sin',
        'sindgen', 'sinh', 'size', 'skewness', 'skip_lun',
        'slicer3', 'slide_image', 'smooth', 'sobel', 'socket',
        'sort', 'spawn', 'spher_harm', 'sph_4pnt', 'sph_scat',
        'spline', 'spline_p', 'spl_init', 'spl_interp', 'sprsab',
        'sprsax', 'sprsin', 'sprstp', 'sqrt', 'standardize',
        'stddev', 'stop', 'strarr', 'strcmp', 'strcompress',
        'streamline', 'stregex', 'stretch', 'string', 'strjoin',
        'strlen', 'strlowcase', 'strmatch', 'strmessage', 'strmid',
        'strpos', 'strput', 'strsplit', 'strtrim', 'struct_assign',
        'struct_hide', 'strupcase', 'surface', 'surfr', 'svdc',
        'svdfit', 'svsol', 'swap_endian', 'swap_endian_inplace',
        'symbol', 'systime', 's_test', 't3d', 'tag_names', 'tan',
        'tanh', 'tek_color', 'temporary', 'tetra_clip',
        'tetra_surface', 'tetra_volume', 'text', 'thin', 'threed',
        'timegen', 'time_test2', 'tm_test', 'total', 'trace',
        'transpose', 'triangulate', 'trigrid', 'triql', 'trired',
        'trisol', 'tri_surf', 'truncate_lun', 'ts_coef', 'ts_diff',
        'ts_fcast', 'ts_smooth', 'tv', 'tvcrs', 'tvlct', 'tvrd',
        'tvscl', 'typename', 't_cvt', 't_pdf', 'uindgen', 'uint',
        'uintarr', 'ul64indgen', 'ulindgen', 'ulon64arr', 'ulonarr',
        'ulong', 'ulong64', 'uniq', 'unsharp_mask', 'usersym',
        'value_locate', 'variance', 'vector', 'vector_field', 'vel',
        'velovect', 'vert_t3d', 'voigt', 'voronoi', 'voxel_proj',
        'wait', 'warp_tri', 'watershed', 'wdelete', 'wf_draw',
        'where', 'widget_base', 'widget_button', 'widget_combobox',
        'widget_control', 'widget_displaycontextmen', 'widget_draw',
        'widget_droplist', 'widget_event', 'widget_info',
        'widget_label', 'widget_list', 'widget_propertysheet',
        'widget_slider', 'widget_tab', 'widget_table',
        'widget_text', 'widget_tree', 'widget_tree_move',
        'widget_window', 'wiener_filter', 'window', 'writeu',
        'write_bmp', 'write_csv', 'write_gif', 'write_image',
        'write_jpeg', 'write_jpeg2000', 'write_nrif', 'write_pict',
        'write_png', 'write_ppm', 'write_spr', 'write_srf',
        'write_sylk', 'write_tiff', 'write_wav', 'write_wave',
        'wset', 'wshow', 'wtn', 'wv_applet', 'wv_cwt',
        'wv_cw_wavelet', 'wv_denoise', 'wv_dwt', 'wv_fn_coiflet',
        'wv_fn_daubechies', 'wv_fn_gaussian', 'wv_fn_haar',
        'wv_fn_morlet', 'wv_fn_paul', 'wv_fn_symlet',
        'wv_import_data', 'wv_import_wavelet', 'wv_plot3d_wps',
        'wv_plot_multires', 'wv_pwt', 'wv_tool_denoise',
        'xbm_edit', 'xdisplayfile', 'xdxf', 'xfont',
        'xinteranimate', 'xloadct', 'xmanager', 'xmng_tmpl',
        'xmtool', 'xobjview', 'xobjview_rotate',
        'xobjview_write_image', 'xpalette', 'xpcolor', 'xplot3d',
        'xregistered', 'xroi', 'xsq_test', 'xsurface', 'xvaredit',
        'xvolume', 'xvolume_rotate', 'xvolume_write_image',
        'xyouts', 'zoom', 'zoom_24')
    """Functions from: http://www.exelisvis.com/docs/routines-1.html"""

    tokens = {
        'root': [
            (r'^\s*;.*?\n', Comment.Single),
            (words(_RESERVED, prefix=r'\b', suffix=r'\b'), Keyword),
            (words(_BUILTIN_LIB, prefix=r'\b', suffix=r'\b'), Name.Builtin),
            (r'\+=|-=|\^=|\*=|/=|#=|##=|<=|>=|=', Operator),
            (r'\+\+|--|->|\+|-|##|#|\*|/|<|>|&&|\^|~|\|\|\?|:', Operator),
            (r'\b(mod=|lt=|le=|eq=|ne=|ge=|gt=|not=|and=|or=|xor=)', Operator),
            (r'\b(mod|lt|le|eq|ne|ge|gt|not|and|or|xor)\b', Operator),
            (r'"[^\"]*"', String.Double),
            (r"'[^\']*'", String.Single),
            (r'\b[+\-]?([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)(D|E)?([+\-]?[0-9]+)?\b',
             Number.Float),
            (r'\b\'[+\-]?[0-9A-F]+\'X(U?(S?|L{1,2})|B)\b', Number.Hex),
            (r'\b\'[+\-]?[0-7]+\'O(U?(S?|L{1,2})|B)\b', Number.Oct),
            (r'\b[+\-]?[0-9]+U?L{1,2}\b', Number.Integer.Long),
            (r'\b[+\-]?[0-9]+U?S?\b', Number.Integer),
            (r'\b[+\-]?[0-9]+B\b', Number),
            (r'.', Text),
        ]
    }

    def analyse_text(text):
        """endelse seems to be unique to IDL, endswitch is rare at least."""
        result = 0

        if 'endelse' in text:
            result += 0.2
        if 'endswitch' in text:
            result += 0.01

        return result