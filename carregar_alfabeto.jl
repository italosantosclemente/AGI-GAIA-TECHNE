function carregar_alfabeto()
    open("ALFABETO.md", "r") do f
        content = read(f, String)
        m = match(r"\[(.*)\]", content)
        if m !== nothing
            s = m[1]
            return [String(m.match) for m in eachmatch(r"\"(.*?)\"", s)]
        else
            error("Alfabeto não encontrado em ALFABETO.md")
        end
    end
end
