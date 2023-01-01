#version 440

in vec2 texCoord;

uniform sampler2D texture0;
uniform int project_id;
uniform int sub_project_id;
uniform int object_id;

layout (location=0) out vec4 out_color;
layout (location=1) out vec4 mouse_picker;

void main() {
	unsigned int max_value = 4294967295;

	vec4 color = texture2D(texture0, texCoord.xy);
	
	out_color = vec4(color.rgb, 1.0);
	//out_color = vec4(0.5, 0.5, 0.5, 1.0);
	mouse_picker = vec4(project_id, ((sub_project_id << 16) + object_id), 0, max_value);
}
