#version 440

in vec2 texCoord;

uniform sampler2D texture0;

layout (location=0) out vec4 out_color;
layout (location=1) out vec4 mouse_picker;

void main() {
	vec4 color = texture2D(texture0, texCoord.xy);
	out_color = vec4(color.rgb, 1.0);
	//out_color = vec4(0.5, 0.5, 0.5, 1.0);
	mouse_picker = vec4(0, 0, 0, 0);
}
