elifePipeline {
    def commit
    stage 'Checkout', {
        checkout scm
        commit = elifeGitRevision()
    }
 
    stage 'Project tests', {
        lock('elife-dashboard--ci') {
            builderDeployRevision 'elife-dashboard--ci', commit
            builderProjectTests 'elife-dashboard--ci', '/srv/elife-article-scheduler'
        }
    }

    stage 'Merge to master', {
        elifeGitMoveToBranch commit, 'master'
    }
}
