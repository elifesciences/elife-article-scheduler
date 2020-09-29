elifePipeline {
    def commit
    stage 'Checkout', {
        checkout scm
        commit = elifeGitRevision()
    }
 
    stage 'Project tests', {
        lock('elife-dashboard--ci') {
            // this would update the elife-dashboard project
            //builderDeployRevision 'elife-dashboard--ci', commit
            //builderProjectTests 'elife-dashboard--ci', '/srv/elife-article-scheduler'

            builderStart "elife-dashboard--ci"
            builderCmd "elife-dashboard--ci", "sudo salt-call state.highstate --retcode-passthrough"
            builderCmd "elife-dashboard--ci", "git reset --hard && git fetch && git checkout ${commit} && ./project_tests.sh", "/srv/elife-article-scheduler", true, "serial"
        }
    }

    stage 'Merge to master', {
        elifeGitMoveToBranch commit, 'master'
    }
}
