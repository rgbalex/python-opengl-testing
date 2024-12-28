#version 150 core
in vec3 Color;
in vec2 Texcoord;

out vec4 outColor;

uniform sampler2D tex;
uniform sampler2D tex2;

void main()
{
    vec4 colTex = texture(tex, Texcoord);
    vec4 colTex2 = texture(tex2, Texcoord);
    outColor = mix(colTex, colTex2, 0.5) * vec4(Color, 1.0);
}