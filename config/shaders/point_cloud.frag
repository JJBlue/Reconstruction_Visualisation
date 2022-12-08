#version 430

in vec3 normal;
in vec3 color;
in vec3 frag_pos;

uniform bool mouse_picker;

out vec4 out_color;

void main() {
	// Settings
	// vec3 light_color = vec3(1.0, 1.0, 1.0);
	// vec3 light_dir = vec3(0.5, 1.0, 0.0);

	// Variables
	// vec3 norm_normal = normalize(normal);
	// vec3 norm_light_dir = normalize(light_dir);

	// Ambient
	// float ambient_strength = 0.3;
	// vec3 ambient = ambient_strength * light_color;

	// Diffuse
	// float diffuse_strength = 0.5;
	// vec3 diffuse = diffuse_strength * light_color * max(dot(norm_normal, norm_light_dir), 0.0);

	// Color
	// vec3 result_color = (ambient + diffuse) * color;
	// out_color = vec4(result_color, 1.0);
	
	if(mouse_picker) {
		int v_id = gl_VertexID;

		int a = v_id & 0xFF
		int b = (v_id >> 8) & 0xFF
		int g = (v_id >> 16) & 0xFF
		int r = (v_id >> 24) & 0xFF

		out_color = vec4(r, g, b, a);
	} else {
		out_color = vec4(color, 1.0);
	}
}
