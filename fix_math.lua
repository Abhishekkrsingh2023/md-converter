function RawInline(el)
    if el.format == "tex" or el.format == "latex" then
        return pandoc.Math("InlineMath", el.text)
    end
end

function RawBlock(el)
    if el.format == "tex" or el.format == "latex" then
        return pandoc.Math("DisplayMath", el.text)
    end
end