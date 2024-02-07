#!/bin/bash

function welcome_msg_ {
    cat << EOF
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
                            CRYSTALProjectTools Setup
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Setup script for CRYSTALProjectTools

Setup date      : `date`
Program         : CRYSTAL
Requirements    : python3
Author          : James Broadhurst (ICL)
--------------------------------------------------------------------------------
EOF
}

function get_scriptdir_ {

    cat << EOF
================================================================================
                                SOURCE DIRECTORY
================================================================================
    By default, the currecnt directory where CRYSTALProjectTools is installed
    will be used as the source directory.

    Default Option:

        `pwd`

EOF

    read -p "    User Option: " SCRIPTDIR

    SCRIPTDIR=${SCRIPTDIR%/}

    if [[ -z ${SCRIPTDIR} ]]; then

        SCRIPTDIR=`pwd`
    
    else

        if [[ ! -d ${SCRIPTDIR} ]]; then

            mkdir -p ${SCRIPTDIR}

        else

            echo "${SCRIPTDIR} already exists, please select a different directory name."
            exit

        fi

        cp -r `pwd`/* ${SCRIPTDIR}

        echo "Files have been copied over. New source directory is ${SCRIPTDIR}"

    fi
}

function band_alias_ {

    read -p "   Band Executable: " BANDEXE

}

function doss_alias_ {

    read -p "   DOSS Executable: " DOSSEXE

}

function check_user_alias_ {
    cat << EOF

--------------------------------------------------------------------------------

    Default alias for the executing the band.py and doss.py files is 'band' and 
    'doss'. If you dont wish to keep these as the standard alias please alter 
    them now otherwise leave the prompts blank

EOF

    band_alias_
    doss_alias_
    

    if [[ ${BANDEXE} == *" "* ]]; then

        echo "ERROR: Please ensure executables do not conatain spaces. Use "_" instead."
        band_alias_
        
    fi

    if [[ ${DOSSEXE} == *" "* ]]; then

        echo "ERROR: Please ensure executables do not conatain spaces. Use "_" instead."
        doss_alias_
        
    fi

    if [[ -z ${BANDEXE} ]]; then

        BANDEXE='band'

    fi

    if [[ -z ${DOSSEXE} ]]; then

        DOSSEXE='doss'

    fi

}

function set_commands_ {
    
    bgline=`grep -nw "# >>> CRYSTALProjectTools >>>" ${HOME}/.bashrc`
    edline=`grep -nw "# <<< CRYSTALProjectTools <<<" ${HOME}/.bashrc`

    if [[ ! -z ${bgline} && ! -z ${edline} ]]; then
        bgline=${bgline%%:*}
        edline=${edline%%:*}
        sed -i "${bgline},${edline}d" ${HOME}/.bashrc
    fi

    echo "# >>> CRYSTALProjectTools >>>" >> ${HOME}/.bashrc
    echo "alias ${BANDEXE}='python3 ${SCRIPTDIR}/band.py'" >> ${HOME}/.bashrc
    echo "alias ${DOSSEXE}='python3 ${SCRIPTDIR}/doss.py'" >> ${HOME}/.bashrc
    echo "# <<< CRYSTALProjectTools <<<" >> ${HOME}/.bashrc

}

function completed_msg_ {
    
    cat << EOF

--------------------------------------------------------------------------------

    Sucessfully setup. To commit the executables to your PATH please run

        source ~/.bashrc

--------------------------------------------------------------------------------
                                    EXITING NOW
--------------------------------------------------------------------------------

EOF

}

function call_command_ {
    welcome_msg_
    get_scriptdir_
    check_user_alias_
    set_commands_
    completed_msg_
}

call_command_