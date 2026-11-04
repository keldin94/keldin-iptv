from pathlib import Path
p=Path("app/src/main/java/com/keldin/iptv/net/M3uParser.java")
s=p.read_text()
old="""    public static Result parse(Reader input, String sourceId, String baseUrl, ProgressListener progress) throws IOException {"""
assert old in s, "Missing parser entry point"
s=s.replace(old,'''    public interface ChannelFilter { boolean include(Channel candidate); }

    public static Result parse(Reader input, String sourceId, String baseUrl,
                               ProgressListener progress) throws IOException {
        return parse(input,sourceId,baseUrl,progress,null);
    }

    public static Result parse(Reader input, String sourceId, String baseUrl,
                               ProgressListener progress,ChannelFilter filter) throws IOException {''',1)
old='''                    result.channels.add(pending);
                    if (progress!=null && result.channels.size()%500==0)
                        progress.onItemsParsed(result.channels.size());
                    if (result.channels.size() >= MAX_CHANNELS)
                        throw new IOException("Lista prelazi granicu od "+MAX_CHANNELS+" stavki. Uvezi manje kategorija ili drugu listu.");'''
assert old in s, "Missing v0.6 parser save marker"
s=s.replace(old,'''                    if(filter==null || filter.include(pending)){
                        result.channels.add(pending);
                        if (progress!=null && result.channels.size()%500==0)
                            progress.onItemsParsed(result.channels.size());
                        if (result.channels.size() >= MAX_CHANNELS)
                            throw new IOException("Too many selected items ("+MAX_CHANNELS+
                              "). Uncheck additional countries or content sections.");
                    }''',1)
p.write_text(s)
print("M3U: category filter is applied before storing entries; oversized input is supported.")
