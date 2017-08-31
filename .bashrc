
# ~/.bashrc: executed by bash(1) for non-login shells.

# If not running interactively, don't do anything
case $- in
	*i*) ;;
	*) return;;
esac

# set variable identifying the chroot you work in (used in the prompt below)
if [[ -z "${debian_chroot:-}" ]] && [[ -r /etc/debian_chroot ]]; then
	debian_chroot=$(cat /etc/debian_chroot)
fi

xhost +local:root > /dev/null 2>&1

for i in ~/.{shells,bash}/*.sh; do
	[[ -f $i ]] && source $i
done 

[ -f ~/.fzf.bash ] && source ~/.fzf.bash
