
[no-exit-message]
[private]
_usage:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}}

[group('常用')]
[no-exit-message]
[positional-arguments]
add *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} add "$@"

[group('常用')]
[no-exit-message]
[positional-arguments]
upgrade *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} upgrade "$@"

[group('常用')]
[no-exit-message]
[positional-arguments]
update *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} update "$@"

[group('常用')]
[no-exit-message]
[positional-arguments]
sync *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} sync "$@"

[group('常用')]
[no-exit-message]
[positional-arguments]
test *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} test "$@"

[group('進階')]
[no-exit-message]
[positional-arguments]
remove *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} remove "$@"

[group('進階')]
[no-exit-message]
[positional-arguments]
dev *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} dev "$@"

[group('進階')]
[no-exit-message]
[positional-arguments]
undev *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} undev "$@"

[group('進階')]
[no-exit-message]
[positional-arguments]
install *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} install "$@"

[group('進階')]
[no-exit-message]
[positional-arguments]
uninstall *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} uninstall "$@"

[group('進階')]
[no-exit-message]
[positional-arguments]
prune *args:
    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}} prune "$@"
