import lz4.block
from ..import EndianBinaryReader

header = """
///////////////////////////////////////////
//
// NOTE: This is *not* a valid shader file
//
///////////////////////////////////////////
"""


class ShaderConverter:
    def Convert(shader) -> str:
        if shader.m_SubProgramBlob: #5.3 - 5.4
            decompressedBytes = lz4.block.decompress(shader.m_SubProgramBlob, shader.decompressedSize)
            return ShaderProgram(EndianBinaryReader(decompressedBytes)).Export(shader.m_Script.decode('utf8'))

        if shader.compressedBlob: #5.5 and up
            return ConvertMultiple(shader)[0]

        return header + shader.m_Script.decode('utf8')

    def ConvertMultiple(shader) -> str:
        if shader.compressedBlob: #5.5 and up
            strs = []
            for i in range(shader.platforms.Length):
                reader = EndianBinaryReader(lz4.block.decompress(shader.compressedBlob[shader.offsets[i] : shader.offsets[i] + shader.compressedLengths[i]], hader.decompressedLengths[i]))
                program = ShaderProgram(reader)
                m_Script = ConvertSerializedShader(shader.m_ParsedForm, shader.platforms[i])
                strs.append(header + program.Export(m_Script))


            return ''.join(str)
        return ""

    def ConvertSerializedShader(m_ParsedForm, platform) -> str: #(SerializedShader, ShaderCompilerPlatform)
        sb = []
        sb.append(f"Shader \"{m_ParsedForm.m_Name}\" {{\n")

        sb.append(ConvertSerializedProperties(m_ParsedForm.m_PropInfo))

        for m_SubShader in m_ParsedForm.m_SubShaders:
            sb.append(ConvertSerializedSubShader(m_SubShader, platform))

        if m_ParsedForm.m_FallbackName:
            sb.append(f"Fallback \"{m_ParsedForm.m_FallbackName}\"\n")

        if m_ParsedForm.m_CustomEditorName:
            sb.append(f"CustomEditor \"{m_ParsedForm.m_CustomEditorName}\"\n")

        sb.append("}")
        return ''.join()

    def ConvertSerializedSubShader(m_SubShader, platform) -> str: #(SerializedSubShader, ShaderCompilerPlatform)
        sb = []
        sb.append("SubShader {\n")
        if m_SubShader.m_LOD != 0:
            sb.append(f" LOD {m_SubShader.m_LOD}\n")

        sb.append(ConvertSerializedTagMap(m_SubShader.m_Tags, 1))

        for m_Passe in m_SubShader.m_Passes:
            sb.append(ConvertSerializedPass(m_Passe, platform))
        sb.append("}\n")
        return ''.join()

    def ConvertSerializedPass(m_Passe, platform) -> str: #(SerializedPass , ShaderCompilerPlatform)
        sb = []
        if m_Passe.m_Type == PassType.kPassTypeNormal:
            sb.append(" Pass ")
        
        elif m_Passe.m_Type == PassType.kPassTypeUse:
                sb.append(" UsePass ")

        elif m_Passe.m_Type == PassType.kPassTypeGrab:
                sb.append(" GrabPass ")

        if m_Passe.m_Type == PassType.kPassTypeUse:
            sb.append(f"\"{m_Passe.m_UseName}\"\n")
        else:
            sb.append("{\n")

            if m_Passe.m_Type == PassType.kPassTypeGrab:
                if m_Passe.m_TextureName:
                    sb.append(f"  \"{m_Passe.m_TextureName}\"\n")

            else:
                sb.append(ConvertSerializedShaderState(m_Passe.m_State))

                if len(m_Passe.progVertex.m_SubPrograms):
                    sb.append("Program \"vp\" {\n")
                    sb.append(ConvertSerializedSubPrograms(m_Passe.progVertex.m_SubPrograms, platform))
                    sb.append("}\n")

                if len(m_Passe.progFragment.m_SubPrograms):
                    sb.append("Program \"fp\" {\n")
                    sb.append(ConvertSerializedSubPrograms(m_Passe.progFragment.m_SubPrograms, platform))
                    sb.append("}\n")

                if len(m_Passe.progGeometry.m_SubPrograms):
                    sb.append("Program \"gp\" {\n")
                    sb.append(ConvertSerializedSubPrograms(m_Passe.progGeometry.m_SubPrograms, platform))
                    sb.append("}\n")

                if len(m_Passe.progHull.m_SubPrograms):
                    sb.append("Program \"hp\" {\n")
                    sb.append(ConvertSerializedSubPrograms(m_Passe.progHull.m_SubPrograms, platform))
                    sb.append("}\n")

                if len(m_Passe.progDomain.m_SubPrograms):
                    sb.append("Program \"dp\" {\n")
                    sb.append(ConvertSerializedSubPrograms(m_Passe.progDomain.m_SubPrograms, platform))
                    sb.append("}\n")

            sb.append("}\n")
        return ''.join(sb)

    def ConvertSerializedSubPrograms(m_SubPrograms, platform)-> str: #(SerializedSubProgram[], ShaderCompilerPlatform)
        sb = []
        groups = {}
        for x in m_SubPrograms:
            if x.m_BlobIndex in groups:
                groups[x.m_BlobIndex].append(x)
            else:
                groups[x.m_BlobIndex]=[x]

        for group in groups.values():
            
            var programs = group.GroupBy(x => x.m_GpuProgramType);
            foreach (var program in programs)
                if CheckGpuProgramUsable(platform, program.Key):
                    var subPrograms = program.ToList();
                    var isTier = subPrograms.Count > 1;
                    foreach (var subProgram in subPrograms)
                        sb.append(f"SubProgram \"{GetPlatformString(platform)} ")
                        if isTier:
                            sb.append(f"hw_tier{subProgram.m_ShaderHardwareTier:00} ")
                        sb.append("\" {\n");
                        sb.append(f"GpuProgramIndex {subProgram.m_BlobIndex}\n")
                        sb.append("}\n");
                    break;


        return ''.join();

    def ConvertSerializedShaderState(SerializedShaderState m_State): #string
        sb = []
        if !string.IsNullOrEmpty(m_State.m_Name):
            sb.append(f"  Name \"{m_State.m_Name}\"\n")
        if m_State.m_LOD != 0:
            sb.append(f"  LOD {m_State.m_LOD}\n")

        sb.append(ConvertSerializedTagMap(m_State.m_Tags, 2));

        sb.append(ConvertSerializedShaderRTBlendState(m_State.rtBlend));

        if m_State.alphaToMask.val > 0f:
            sb.append("  AlphaToMask On\n");

        if m_State.zClip?.val != 1f: #ZClip On
            sb.append("  ZClip Off\n");

        if m_State.zTest.val != 4f: #ZTest LEqual
            sb.append("  ZTest ");
            switch (m_State.zTest.val) //enum CompareFunction
                case 0f: //kFuncDisabled
                    sb.append("Off");
                    break;
                case 1f: //kFuncNever
                    sb.append("Never");
                    break;
                case 2f: //kFuncLess
                    sb.append("Less");
                    break;
                case 3f: //kFuncEqual
                    sb.append("Equal");
                    break;
                case 5f: //kFuncGreater
                    sb.append("Greater");
                    break;
                case 6f: //kFuncNotEqual
                    sb.append("NotEqual");
                    break;
                case 7f: //kFuncGEqual
                    sb.append("GEqual");
                    break;
                case 8f: //kFuncAlways
                    sb.append("Always");
                    break;

            sb.append("\n");

        if m_State.zWrite.val != 1f: #ZWrite On
            sb.append("  ZWrite Off\n");

        if m_State.culling.val != 2f: #Cull Back
            sb.append("  Cull ");
            switch (m_State.culling.val) //enum CullMode
                case 0f: //kCullOff
                    sb.append("Off");
                    break;
                case 1f: //kCullFront
                    sb.append("Front");
                    break;
            sb.append("\n");

        if m_State.offsetFactor.val != 0f || m_State.offsetUnits.val != 0f:
            sb.append(f"  Offset {m_State.offsetFactor.val}, {m_State.offsetUnits.val}\n")

        //TODO Stencil

        //TODO Fog

        if m_State.lighting:
            sb.append(f"  Lighting {(m_State.lighting ? "On" : "Off")}\n")

        sb.append(f"  GpuProgramID {m_State.gpuProgramID}\n")

        return ''.join();

    def ConvertSerializedShaderRTBlendState(SerializedShaderRTBlendState[] rtBlend): #string
        //TODO Blend
        sb = []
        /*for (var i = 0; i < rtBlend.Length; i++)
            var blend = rtBlend[i];
            if (!blend.srcBlend.val.Equals(1f) ||
                !blend.destBlend.val.Equals(0f) ||
                !blend.srcBlendAlpha.val.Equals(1f) ||
                !blend.destBlendAlpha.val.Equals(0f))
                sb.append("  Blend ");
                sb.append(f"{i} ")
                sb.append('\n');
        }*/

        return ''.join();

    def ConvertSerializedTagMap(SerializedTagMap m_Tags, int intent): #string
        sb = []
        if m_Tags.tags.Length > 0:
            sb.append(new string(' ', intent));
            sb.append("Tags { ");
            foreach (var pair in m_Tags.tags)
                sb.append(f"\"{pair.Key}\" = \"{pair.Value}\" ")
            sb.append("}\n");
        return ''.join();

    def ConvertSerializedProperties(SerializedProperties m_PropInfo): #string
        sb = []
        sb.append("Properties {\n");
        foreach (var m_Prop in m_PropInfo.m_Props)
            sb.append(ConvertSerializedProperty(m_Prop));
        sb.append("}\n");
        return ''.join();

    def ConvertSerializedProperty(SerializedProperty m_Prop): #string
        sb = []
        foreach (var m_Attribute in m_Prop.m_Attributes)
            sb.append(f"[{m_Attribute}] ")
        //TODO Flag
        sb.append(f"{m_Prop.m_Name} (\"{m_Prop.m_Description}\", ")
        switch (m_Prop.m_Type)
            case SerializedPropertyType.kColor:
                sb.append("Color");
                break;
            case SerializedPropertyType.kVector:
                sb.append("Vector");
                break;
            case SerializedPropertyType.kFloat:
                sb.append("Float");
                break;
            case SerializedPropertyType.kRange:
                sb.append(f"Range({m_Prop.m_DefValue[1]}, {m_Prop.m_DefValue[2]})")
                break;
            case SerializedPropertyType.kTexture:
                switch (m_Prop.m_DefTexture.m_TexDim)
                    case TextureDimension.kTexDimAny:
                        sb.append("any");
                        break;
                    case TextureDimension.kTexDim2D:
                        sb.append("2D");
                        break;
                    case TextureDimension.kTexDim3D:
                        sb.append("3D");
                        break;
                    case TextureDimension.kTexDimCUBE:
                        sb.append("Cube");
                        break;
                    case TextureDimension.kTexDim2DArray:
                        sb.append("2DArray");
                        break;
                    case TextureDimension.kTexDimCubeArray:
                        sb.append("CubeArray");
                        break;
                break;
        sb.append(") = ");
        switch (m_Prop.m_Type)
            case SerializedPropertyType.kColor:
            case SerializedPropertyType.kVector:
                sb.append(f"({m_Prop.m_DefValue[0]},{m_Prop.m_DefValue[1]},{m_Prop.m_DefValue[2]},{m_Prop.m_DefValue[3]})")
                break;
            case SerializedPropertyType.kFloat:
            case SerializedPropertyType.kRange:
                sb.append(m_Prop.m_DefValue[0]);
                break;
            case SerializedPropertyType.kTexture:
                sb.append(f"\"{m_Prop.m_DefTexture.m_DefaultName}\" {{ }}")
                break;
            default:
                throw new ArgumentOutOfRangeException();
        sb.append("\n");
        return ''.join();

    def CheckGpuProgramUsable(ShaderCompilerPlatform platform, ShaderGpuProgramType programType): #bool
        switch (platform)
            case ShaderCompilerPlatform.kShaderCompPlatformGL:
                return programType == ShaderGpuProgramType.kShaderGpuProgramGLLegacy;
            case ShaderCompilerPlatform.kShaderCompPlatformD3D9:
                return programType == ShaderGpuProgramType.kShaderGpuProgramDX9VertexSM20
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX9VertexSM30
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX9PixelSM20
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX9PixelSM30;
            case ShaderCompilerPlatform.kShaderCompPlatformXbox360:
                return programType == ShaderGpuProgramType.kShaderGpuProgramConsole;
            case ShaderCompilerPlatform.kShaderCompPlatformPS3:
                return programType == ShaderGpuProgramType.kShaderGpuProgramConsole;
            case ShaderCompilerPlatform.kShaderCompPlatformD3D11:
                return programType == ShaderGpuProgramType.kShaderGpuProgramDX11VertexSM40
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX11VertexSM50
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX11PixelSM40
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX11PixelSM50
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX11GeometrySM40
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX11GeometrySM50
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX11HullSM50
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX11DomainSM50;
            case ShaderCompilerPlatform.kShaderCompPlatformGLES20:
                return programType == ShaderGpuProgramType.kShaderGpuProgramGLES;
            case ShaderCompilerPlatform.kShaderCompPlatformNaCl: //Obsolete
                throw new NotSupportedException();
            case ShaderCompilerPlatform.kShaderCompPlatformFlash: //Obsolete
                throw new NotSupportedException();
            case ShaderCompilerPlatform.kShaderCompPlatformD3D11_9x:
                return programType == ShaderGpuProgramType.kShaderGpuProgramDX10Level9Vertex
                    || programType == ShaderGpuProgramType.kShaderGpuProgramDX10Level9Pixel;
            case ShaderCompilerPlatform.kShaderCompPlatformGLES3Plus:
                return programType == ShaderGpuProgramType.kShaderGpuProgramGLES31AEP
                    || programType == ShaderGpuProgramType.kShaderGpuProgramGLES31
                    || programType == ShaderGpuProgramType.kShaderGpuProgramGLES3;
            case ShaderCompilerPlatform.kShaderCompPlatformPSP2:
                return programType == ShaderGpuProgramType.kShaderGpuProgramConsole;
            case ShaderCompilerPlatform.kShaderCompPlatformPS4:
                return programType == ShaderGpuProgramType.kShaderGpuProgramConsole;
            case ShaderCompilerPlatform.kShaderCompPlatformXboxOne:
                return programType == ShaderGpuProgramType.kShaderGpuProgramConsole;
            case ShaderCompilerPlatform.kShaderCompPlatformPSM: //Unknown
                throw new NotSupportedException();
            case ShaderCompilerPlatform.kShaderCompPlatformMetal:
                return programType == ShaderGpuProgramType.kShaderGpuProgramMetalVS
                    || programType == ShaderGpuProgramType.kShaderGpuProgramMetalFS;
            case ShaderCompilerPlatform.kShaderCompPlatformOpenGLCore:
                return programType == ShaderGpuProgramType.kShaderGpuProgramGLCore32
                    || programType == ShaderGpuProgramType.kShaderGpuProgramGLCore41
                    || programType == ShaderGpuProgramType.kShaderGpuProgramGLCore43;
            case ShaderCompilerPlatform.kShaderCompPlatformN3DS:
                return programType == ShaderGpuProgramType.kShaderGpuProgramConsole;
            case ShaderCompilerPlatform.kShaderCompPlatformWiiU:
                return programType == ShaderGpuProgramType.kShaderGpuProgramConsole;
            case ShaderCompilerPlatform.kShaderCompPlatformVulkan:
                return programType == ShaderGpuProgramType.kShaderGpuProgramSPIRV;
            case ShaderCompilerPlatform.kShaderCompPlatformSwitch:
                return programType == ShaderGpuProgramType.kShaderGpuProgramConsole;
            case ShaderCompilerPlatform.kShaderCompPlatformXboxOneD3D12:
                return programType == ShaderGpuProgramType.kShaderGpuProgramConsole;
            default:
                throw new NotSupportedException();


    def GetPlatformString(ShaderCompilerPlatform platform): #string
        switch (platform)
            case ShaderCompilerPlatform.kShaderCompPlatformGL:
                return "openGL";
            case ShaderCompilerPlatform.kShaderCompPlatformD3D9:
                return "d3d9";
            case ShaderCompilerPlatform.kShaderCompPlatformXbox360:
                return "xbox360";
            case ShaderCompilerPlatform.kShaderCompPlatformPS3:
                return "ps3";
            case ShaderCompilerPlatform.kShaderCompPlatformD3D11:
                return "d3d11";
            case ShaderCompilerPlatform.kShaderCompPlatformGLES20:
                return "gles";
            case ShaderCompilerPlatform.kShaderCompPlatformNaCl:
                return "glesdesktop";
            case ShaderCompilerPlatform.kShaderCompPlatformFlash:
                return "flash";
            case ShaderCompilerPlatform.kShaderCompPlatformD3D11_9x:
                return "d3d11_9x";
            case ShaderCompilerPlatform.kShaderCompPlatformGLES3Plus:
                return "gles3";
            case ShaderCompilerPlatform.kShaderCompPlatformPSP2:
                return "psp2";
            case ShaderCompilerPlatform.kShaderCompPlatformPS4:
                return "ps4";
            case ShaderCompilerPlatform.kShaderCompPlatformXboxOne:
                return "xboxone";
            case ShaderCompilerPlatform.kShaderCompPlatformPSM:
                return "psm";
            case ShaderCompilerPlatform.kShaderCompPlatformMetal:
                return "metal";
            case ShaderCompilerPlatform.kShaderCompPlatformOpenGLCore:
                return "glcore";
            case ShaderCompilerPlatform.kShaderCompPlatformN3DS:
                return "n3ds";
            case ShaderCompilerPlatform.kShaderCompPlatformWiiU:
                return "wiiu";
            case ShaderCompilerPlatform.kShaderCompPlatformVulkan:
                return "vulkan";
            case ShaderCompilerPlatform.kShaderCompPlatformSwitch:
                return "switch";
            case ShaderCompilerPlatform.kShaderCompPlatformXboxOneD3D12:
                return "xboxone_d3d12";
            default:
                return "unknown";



public class ShaderProgram
    private ShaderSubProgram[] m_SubPrograms;

    public ShaderProgram(BinaryReader reader)
        var subProgramsCapacity = reader.ReadInt32();
        m_SubPrograms = new ShaderSubProgram[subProgramsCapacity];
        for (int i = 0; i < subProgramsCapacity; i++)
            reader.BaseStream.Position = 4 + i * 8;
            var offset = reader.ReadInt32();
            reader.BaseStream.Position = offset;
            m_SubPrograms[i] = new ShaderSubProgram(reader);


    public string Export(string shader)
        var evaluator = new MatchEvaluator(match =>
            var index = int.Parse(match.Groups[1].Value);
            return m_SubPrograms[index].Export();
        });
        shader = Regex.Replace(shader, "GpuProgramIndex (.+)", evaluator);
        return shader;
}

public class ShaderSubProgram
    private int m_Version;
    public ShaderGpuProgramType m_ProgramType;
    public string[] m_Keywords;
    public string[] m_LocalKeywords;
    public byte[] m_ProgramCode;

    public ShaderSubProgram(BinaryReader reader)
        //LoadGpuProgramFromData
        //201509030 - Unity 5.3
        //201510240 - Unity 5.4
        //201608170 - Unity 5.5
        //201609010 - Unity 5.6, 2017.1 & 2017.2
        //201708220 - Unity 2017.3, Unity 2017.4 & Unity 2018.1
        //201802150 - Unity 2018.2 & Unity 2018.3
        //201806140 - Unity 2019.1
        m_Version = reader.ReadInt32();
        m_ProgramType = (ShaderGpuProgramType)reader.ReadInt32();
        reader.BaseStream.Position += 12;
        if m_Version >= 201608170:
            reader.BaseStream.Position += 4;
        var m_KeywordsSize = reader.ReadInt32();
        m_Keywords = new string[m_KeywordsSize];
        for (int i = 0; i < m_KeywordsSize; i++)
            m_Keywords[i] = reader.ReadAlignedString();
        if m_Version >= 201806140:
            var m_LocalKeywordsSize = reader.ReadInt32();
            m_LocalKeywords = new string[m_LocalKeywordsSize];
            for (int i = 0; i < m_LocalKeywordsSize; i++)
                m_LocalKeywords[i] = reader.ReadAlignedString();

        m_ProgramCode = reader.ReadBytes(reader.ReadInt32());
        reader.AlignStream();

        //TODO

    public string Export()
        sb = []
        if m_Keywords.Length > 0:
            sb.append("Keywords { ");
            foreach (string keyword in m_Keywords)
                sb.append(f"\"{keyword}\" ")
            sb.append("}\n");

        sb.append("\"");
        if m_ProgramCode.Length > 0:
            switch (m_ProgramType)
                case ShaderGpuProgramType.kShaderGpuProgramGLLegacy:
                case ShaderGpuProgramType.kShaderGpuProgramGLES31AEP:
                case ShaderGpuProgramType.kShaderGpuProgramGLES31:
                case ShaderGpuProgramType.kShaderGpuProgramGLES3:
                case ShaderGpuProgramType.kShaderGpuProgramGLES:
                case ShaderGpuProgramType.kShaderGpuProgramGLCore32:
                case ShaderGpuProgramType.kShaderGpuProgramGLCore41:
                case ShaderGpuProgramType.kShaderGpuProgramGLCore43:
                    sb.append(Encoding.UTF8.GetString(m_ProgramCode));
                    break;
                case ShaderGpuProgramType.kShaderGpuProgramDX9VertexSM20:
                case ShaderGpuProgramType.kShaderGpuProgramDX9VertexSM30:
                case ShaderGpuProgramType.kShaderGpuProgramDX9PixelSM20:
                case ShaderGpuProgramType.kShaderGpuProgramDX9PixelSM30:
                        /*var shaderBytecode = new ShaderBytecode(m_ProgramCode);
                        sb.append(shaderBytecode.Disassemble());*/
                        sb.append("// shader disassembly not supported on DXBC");
                        break;
                case ShaderGpuProgramType.kShaderGpuProgramDX10Level9Vertex:
                case ShaderGpuProgramType.kShaderGpuProgramDX10Level9Pixel:
                case ShaderGpuProgramType.kShaderGpuProgramDX11VertexSM40:
                case ShaderGpuProgramType.kShaderGpuProgramDX11VertexSM50:
                case ShaderGpuProgramType.kShaderGpuProgramDX11PixelSM40:
                case ShaderGpuProgramType.kShaderGpuProgramDX11PixelSM50:
                case ShaderGpuProgramType.kShaderGpuProgramDX11GeometrySM40:
                case ShaderGpuProgramType.kShaderGpuProgramDX11GeometrySM50:
                case ShaderGpuProgramType.kShaderGpuProgramDX11HullSM50:
                case ShaderGpuProgramType.kShaderGpuProgramDX11DomainSM50:
                        int start = 6;
                        if m_Version == 201509030: # 5.3
                            start = 5;
                        var buff = new byte[m_ProgramCode.Length - start];
                        Buffer.BlockCopy(m_ProgramCode, start, buff, 0, buff.Length);
                        /*var shaderBytecode = new ShaderBytecode(buff);
                        sb.append(shaderBytecode.Disassemble());*/
                        sb.append("// shader disassembly not supported on DXBC");
                        break;
                case ShaderGpuProgramType.kShaderGpuProgramMetalVS:
                case ShaderGpuProgramType.kShaderGpuProgramMetalFS:
                    using (var reader = new BinaryReader(new MemoryStream(m_ProgramCode)))
                        var fourCC = reader.ReadUInt32();
                        if fourCC == 0xf00dcafe:
                            int offset = reader.ReadInt32();
                            reader.BaseStream.Position = offset;
                        var entryName = reader.ReadStringToNull();
                        var buff = reader.ReadBytes((int)(reader.BaseStream.Length - reader.BaseStream.Position));
                        sb.append(Encoding.UTF8.GetString(buff));
                    break;
                case ShaderGpuProgramType.kShaderGpuProgramSPIRV:
                    sb.append("// shader disassembly not supported on SPIR-V\n");
                    sb.append("// https://github.com/KhronosGroup/SPIRV-Cross");
                    break;
                case ShaderGpuProgramType.kShaderGpuProgramConsole:
                    sb.append(Encoding.UTF8.GetString(m_ProgramCode));
                    break;
                default:
                    sb.append(f"//shader disassembly not supported on {m_ProgramType}")
                    break;

        sb.append('"');
        return ''.join();
}
